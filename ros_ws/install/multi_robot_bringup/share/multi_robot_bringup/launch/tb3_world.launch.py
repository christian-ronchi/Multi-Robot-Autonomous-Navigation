import os
import yaml

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    AppendEnvironmentVariable,
    IncludeLaunchDescription,
    DeclareLaunchArgument,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node

from multi_robot_scripts.utils import load_sdf_with_namespace, create_namespaced_bridge_yaml

def generate_launch_description():
    """
    Launches a multi-robot simulation with multiple TurtleBot3 robots in a Gazebo world.
    
    This launch file handles the following:
    - Starts the Gazebo simulation server and client.
    - Spawns multiple TurtleBot3 robots based on a configuration file.
    - Sets up the robot state publisher for each robot to publish TF transforms.
    - Establishes a ROS 2 <-> Gazebo bridge for each robot's topics.
    - Starts a single, global bridge for the /clock topic to ensure consistent simulation time.
    """
    # Get the share directory for relevant packages
    pkg_multi_robot_bringup = get_package_share_directory('multi_robot_bringup')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    pkg_turtlebot3_gazebo = get_package_share_directory('turtlebot3_gazebo')

    # Declare launch arguments
    # use_sim_time is set to 'true' to use the simulation clock from Gazebo
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    world_path = LaunchConfiguration('world')

    # Path to the Gazebo world file
    # world_path = os.path.join(pkg_turtlebot3_gazebo, 'worlds', 'turtlebot3_dqn_stage1.world')
    default_world_path = os.path.join(pkg_turtlebot3_gazebo, 'worlds', 'turtlebot3_dqn_stage1.world')

    declare_world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world_path,
        description='Full path to the world file to load.'
    )

    # Initialize the main launch description and add the world argument
    ld = LaunchDescription() 
    ld.add_action(declare_world_arg)
    
    # Launch Gazebo server and client
    # The `gz_sim.launch.py` is included twice: once for the server (`-s`) and once for the client (`-g`).
    # This allows for separate control and logging of the server and GUI.
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': ['-r -s -v2 ', world_path], 'on_exit_shutdown': 'true'}.items()
    )
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': '-g -v2', 'on_exit_shutdown': 'true'}.items()
    )

    # Add Gazebo server/client to the launch description
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)

    # Load robot configurations from the YAML file
    robot_config_path = os.path.join(pkg_multi_robot_bringup, 'config', 'robots.yaml')
    with open(robot_config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Filter the list to include only robots marked as 'enabled'
    robots = [r for r in config['robots'] if r.get('enabled', True)]
    
    # Determine the TurtleBot3 model from an environment variable, defaulting to 'burger'
    tb3_model = os.environ.get('TURTLEBOT3_MODEL', 'burger')
    model_dir = f'turtlebot3_{tb3_model}'
    
    # Construct the path to the robot's URDF file
    urdf_file_name = 'turtlebot3_' + tb3_model + '.urdf'
    urdf_path = os.path.join(
        pkg_turtlebot3_gazebo,
        'urdf',
        urdf_file_name)

    # Read the URDF file content, which will be used by robot_state_publisher
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    # Iterate through each enabled robot to create and launch its nodes
    for robot in robots:
        namespace = robot['name']
        
        # Patch the robot's SDF file with its unique namespace to avoid topic and frame conflicts
        sdf_path = os.path.join(pkg_turtlebot3_gazebo, 'models', model_dir, 'model.sdf')
        patched_sdf = load_sdf_with_namespace(sdf_path, namespace)

        # Create a robot_state_publisher node for each robot
        # It publishes the robot's TF tree based on its URDF.
        # The 'frame_prefix' ensures that all frames are namespaced (e.g., 'tb1/base_link').
        # TF topics are remapped to the global /tf and /tf_static for a unified TF tree.
        robot_state_publisher = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace=namespace,
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'robot_description': robot_desc},
                {'frame_prefix': namespace + '/'}
            ],
            remappings=[
                ('tf', '/tf'),
                ('tf_static', '/tf_static')
            ]
        )

        # Create a spawner node to add the robot model to the Gazebo simulation
        # The patched SDF string is used to define the model.
        spawner_node = Node(
            package='ros_gz_sim',
            executable='create',
            namespace=namespace,
            arguments=[
                '-name', f'{namespace}_{tb3_model}',
                '-string', patched_sdf,
                '-x', str(robot['x_pose']),
                '-y', str(robot['y_pose']),
                '-z', str(robot['z_pose']),
            ],
            output='screen',
        )

        # ROS 2 <-> Gazebo Bridge Node
        # Establishes communication for topics like cmd_vel, odometry, and sensor data.
        bridge_template = os.path.join(pkg_turtlebot3_gazebo, 'params', f'turtlebot3_{tb3_model}_bridge.yaml')
        namespaced_bridge = create_namespaced_bridge_yaml(bridge_template, namespace)

        bridge_node = Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name=f'{namespace}_bridge',
            arguments=['--ros-args', '-p', f'config_file:={namespaced_bridge}'],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen',
        )

        # Add the robot's nodes to the launch description
        ld.add_action(robot_state_publisher)
        ld.add_action(spawner_node)
        ld.add_action(bridge_node)

    # Create a single, global bridge for the /clock topic
    # This ensures all ROS nodes use a consistent simulation time from Gazebo.
    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='clock_bridge',
        output='screen',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        parameters=[{'use_sim_time': use_sim_time}],
    )
    ld.add_action(clock_bridge)

    # Add the Gazebo model path to the environment variables
    # This allows Gazebo to locate the TurtleBot3 model files.
    ld.add_action(AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.join(pkg_turtlebot3_gazebo, 'models'))
    )

    return ld