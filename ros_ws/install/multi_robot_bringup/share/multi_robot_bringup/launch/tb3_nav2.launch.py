import os
import yaml

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    LogInfo
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, LifecycleNode
from launch_ros.substitutions import FindPackageShare
from multi_robot_scripts.utils import generate_rviz_config, generate_namespaced_nav2_params

def generate_launch_description():
    """
    Generate the launch description for a multi-robot navigation setup using Nav2.

    This function creates a launch description that:
    -  Sets up file paths for configurations, maps, and RViz.
    -  Declares launch arguments for map path and simulation time.
    -  Launches a single, global map_server to serve the map to all robots.
    -  Reads a robot configuration file to determine which robots to launch.
    -  For each enabled robot, it:
        - Generates a namespaced Nav2 parameter file.
        - Generates a namespaced RViz configuration file.
        - Launches the full Nav2 stack (AMCL, controller, planner, etc.) within the robot's namespace.
        - Launches a lifecycle manager to manage the robot's Nav2 nodes.
        - Launches an RViz instance configured for that specific robot.
    """
    # Set up paths and environment variables
    pkg_multi_robot_bringup = get_package_share_directory('multi_robot_bringup')
    robot_config_path = os.path.join(pkg_multi_robot_bringup, 'config', 'robots.yaml')
    rviz_template_path = os.path.join(pkg_multi_robot_bringup, 'rviz', 'tb3_navigation2.rviz')
    default_map_path = os.path.join(pkg_multi_robot_bringup, 'map', 'map2.yaml')

    # Get the TurtleBot3 model from the environment variable, defaulting to 'burger'
    tb3_model = os.environ.get('TURTLEBOT3_MODEL', 'burger')

    # Construct the path to the Nav2 parameters file based on the robot model
    param_file_name = f"{tb3_model}_nav2_params.yaml"
    param_file_path = os.path.join(pkg_multi_robot_bringup, 'params', param_file_name)

    # Declare launch arguments
    declare_map_arg = DeclareLaunchArgument(
        'map',
        default_value=default_map_path,
        description='Full path to the map file to load.'
    )
    declare_use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    # Create the main launch description and add arguments
    ld = LaunchDescription()
    ld.add_action(declare_map_arg)
    ld.add_action(declare_use_sim_time_arg)
    
    # Get the launch argument values
    map_path = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Launch the global map server
    # A single map_server is launched in the global namespace to serve the map
    # to all robots, preventing conflicts from multiple publishers on the /map topic.
    lifecycle_nodes = ['map_server']

    map_server_node = LifecycleNode(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        namespace='',
        output='screen',
        parameters=[
            param_file_path,
            {'use_sim_time': use_sim_time},
            {'yaml_filename': map_path}
        ]
    )

    lifecycle_manager_map = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_map',
        namespace='',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'autostart': True},
            {'node_names': lifecycle_nodes}
        ]
    )

    ld.add_action(map_server_node)
    ld.add_action(lifecycle_manager_map)

    # Load robot configurations and launch per-robot nodes
    with open(robot_config_path, 'r') as f:
        robots = [r for r in yaml.safe_load(f)['robots'] if r.get('enabled', True)]

    for robot in robots:
        robot_name = robot['name']
 
        # Generate namespaced configuration files for this robot
        rviz_config = generate_rviz_config(robot_name, rviz_template_path)
        namespaced_params = generate_namespaced_nav2_params(param_file_path, robot_name)

        ld.add_action(LogInfo(msg=[f'[Launch] Using namespaced param file for {robot_name}: ', namespaced_params]))

        # Remap TF topics to the global /tf and /tf_static topics. This is crucial
        # for having a single, unified TF tree that all nodes can use.
        remappings = [('tf', '/tf'), ('tf_static', '/tf_static')]
        
        # Define the list of lifecycle nodes for this robot's Nav2 stack
        robot_lifecycle_nodes = [
            'amcl',
            'controller_server',
            'planner_server',
            'behavior_server',
            'bt_navigator',
            'waypoint_follower',
            'velocity_smoother',
            'collision_monitor'
        ]

        # Resolve the path to the behavior tree XML file at launch time
        bt_xml_path = PathJoinSubstitution([
            FindPackageShare('nav2_bt_navigator'),
            'behavior_trees',
            'navigate_to_pose_w_replanning_and_recovery.xml'
        ])

        # Create the Nav2 stack nodes for the current robot
        nav2_nodes = [
            LifecycleNode(
                package='nav2_amcl',
                executable='amcl',
                name='amcl',
                namespace=robot_name,
                output='screen',
                parameters=[namespaced_params, {'use_sim_time': use_sim_time}],
                remappings=remappings
            ),
            LifecycleNode(
                package='nav2_controller',
                executable='controller_server',
                name='controller_server',
                namespace=robot_name,
                output='screen',
                parameters=[namespaced_params, {'use_sim_time': use_sim_time}],
                remappings=remappings
            ),
            LifecycleNode(
                package='nav2_planner',
                executable='planner_server',
                name='planner_server',
                namespace=robot_name,
                output='screen',
                parameters=[namespaced_params, {'use_sim_time': use_sim_time}],
                remappings=remappings
            ),
            LifecycleNode(
                package='nav2_behaviors',
                executable='behavior_server',
                name='behavior_server',
                namespace=robot_name,
                output='screen',
                parameters=[namespaced_params, {'use_sim_time': use_sim_time}],
                remappings=remappings
            ),
            LifecycleNode(
                package='nav2_bt_navigator',
                executable='bt_navigator',
                name='bt_navigator',
                namespace=robot_name,
                output='screen',
                parameters=[
                    namespaced_params,
                    {'use_sim_time': use_sim_time},
                    {'default_nav_to_pose_bt_xml': bt_xml_path},
                    {'default_nav_through_poses_bt_xml': bt_xml_path}
                ],
                remappings=remappings
            ),
            LifecycleNode(
                package='nav2_waypoint_follower',
                executable='waypoint_follower',
                name='waypoint_follower',
                namespace=robot_name,
                output='screen',
                parameters=[namespaced_params, {'use_sim_time': use_sim_time}],
                remappings=remappings
            ),
            LifecycleNode(
                package='nav2_velocity_smoother',
                executable='velocity_smoother',
                name='velocity_smoother',
                namespace=robot_name,
                output='screen',
                parameters=[namespaced_params, {'use_sim_time': use_sim_time}],
                remappings=remappings
            ),
            LifecycleNode(
                package='nav2_collision_monitor',
                executable='collision_monitor',
                name='collision_monitor',
                namespace=robot_name,
                output='screen',
                parameters=[namespaced_params, {'use_sim_time': use_sim_time}],
                remappings=remappings
            )
        ]

        # Create an RViz node for this robot
        rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            namespace=robot_name,
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': use_sim_time}],
            remappings=remappings,
            output='screen'
        )

        # Create a lifecycle manager for this robot's Nav2 stack
        lifecycle_manager_nav = Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            namespace=robot_name,
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'autostart': True},
                {'node_names': robot_lifecycle_nodes}
            ]
        )

        # Create an obstacle detector node for this robot
        obstacle_detector_node = Node(
            package='dynamic_obstacle_detector',
            executable='obstacle_detector_node',
            name='obstacle_detector_node',
            namespace=robot_name,
            output='screen',
            parameters=[
                {'use_sim_time': use_sim_time},
                {'robot_id': robot_name},
                {'target_frame': f'{robot_name}/odom'},
            ],
            remappings=remappings
        )

        # Add all nodes and the lifecycle manager for this robot to the launch description
        for node in nav2_nodes:
            ld.add_action(node)
        
        ld.add_action(lifecycle_manager_nav)
        ld.add_action(rviz_node)
        ld.add_action(obstacle_detector_node)

    return ld