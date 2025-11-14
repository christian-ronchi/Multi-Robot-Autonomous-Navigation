import os
import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, LifecycleNode
from launch_ros.substitutions import FindPackageShare
from slam_scripts.utils import generate_rviz_config, generate_namespaced_nav2_params

def generate_launch_description():
    """
    Generate the launch description for a multi-robot navigation setup using Nav2.

    This function creates a launch description that:
    -  Sets up file paths for configurations, maps, and RViz.
    -  Declares launch arguments for simulation time.
    -  Reads a robot configuration file to determine which robots are enabled.
    -  For each enabled robot, it: 
        - Launches a namespaced Nav2 stack for navigation.
        - Manages the lifecycle of the Nav2 nodes.
        - Launches a namespaced RViz instance for visualization.
    """
    # Set up paths and environment variables
    pkg_turtlebot3_gazebo = get_package_share_directory('turtlebot3_gazebo')
    pkg_slam_multi_robot = get_package_share_directory('slam_multi_robot')
    pkg_multi_robot_bringup = get_package_share_directory('multi_robot_bringup')
    robot_config_path = os.path.join(pkg_multi_robot_bringup, 'config', 'robots.yaml')
    rviz_template_path = os.path.join(pkg_slam_multi_robot, 'rviz', 'tb3_navigation2.rviz')
    params_template = os.path.join(pkg_slam_multi_robot, 'params', 'params_nav2.yaml')
  
    # Get the TurtleBot3 model from an environment variable, defaulting to 'burger'.
    # This is not directly used here but is good practice to have for context.
    tb3_model = os.environ.get('TURTLEBOT3_MODEL', 'burger')

    # Declare the 'use_sim_time' launch argument
    declare_use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    # Create the main launch description and add arguments
    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time_arg)
    
    # Get the value of the 'use_sim_time' launch argument
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Load robot configurations from the YAML file and filter for enabled robots
    with open(robot_config_path, 'r') as f:
        robots = [r for r in yaml.safe_load(f)['robots'] if r.get('enabled', True)]

    for robot in robots:
        robot_name = robot['name']
 
        # Generate namespaced configuration files for this robot
        rviz_config = generate_rviz_config(robot_name, rviz_template_path)
        params_file = generate_namespaced_nav2_params(params_template, robot_name)

        # Remap TF topics to the global /tf and /tf_static topics. This is crucial
        # for having a single, unified TF tree that all nodes can use.
        remappings = [('tf', '/tf'), ('tf_static', '/tf_static')]

        # Define the list of lifecycle nodes for this robot's Nav2 stack
        robot_lifecycle_nodes = [
            'controller_server',
            'planner_server',
            'behavior_server',
            'bt_navigator',
            'waypoint_follower',
            'velocity_smoother',
            'collision_monitor',
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
                package='nav2_controller',
                executable='controller_server',
                name='controller_server',
                namespace=robot_name,
                output='screen',
                parameters=[params_file, {'use_sim_time': use_sim_time}],
                remappings=remappings
            ),
            LifecycleNode(
                package='nav2_planner',
                executable='planner_server',
                name='planner_server',
                namespace=robot_name,
                output='screen',
                parameters=[params_file, {'use_sim_time': use_sim_time}],
                remappings=remappings
            ),
            LifecycleNode(
                package='nav2_behaviors',
                executable='behavior_server',
                name='behavior_server',
                namespace=robot_name,
                output='screen',
                parameters=[params_file, {'use_sim_time': use_sim_time}],
                remappings=remappings + [('local_costmap', 'local_costmap/costmap_raw')]
            ),
            LifecycleNode(
                package='nav2_bt_navigator',
                executable='bt_navigator',
                name='bt_navigator',
                namespace=robot_name,
                output='screen',
                parameters=[
                    params_file,
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
                parameters=[params_file, {'use_sim_time': use_sim_time}],
                remappings=remappings
            ),
            LifecycleNode(
                package='nav2_velocity_smoother',
                executable='velocity_smoother',
                name='velocity_smoother',
                namespace=robot_name,
                output='screen',
                parameters=[params_file, {'use_sim_time': use_sim_time}],
                remappings=remappings + [
                    ("cmd_vel", "cmd_vel_nav"),
                    ("cmd_vel_smoothed", "cmd_vel")
                ]
            ),
            LifecycleNode(
                package='nav2_collision_monitor',
                executable='collision_monitor',
                name='collision_monitor',
                namespace=robot_name,
                output='screen',
                parameters=[params_file, {'use_sim_time': use_sim_time}],
                remappings=remappings
            ),
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
                {'autostart': True},  # Automatically start the lifecycle nodes
                {'node_names': robot_lifecycle_nodes}
            ]
        )

        # Add all nodes for this robot to the launch description
        for node in nav2_nodes:
            ld.add_action(node)
        
        ld.add_action(lifecycle_manager_nav)
        ld.add_action(rviz_node)
        
    return ld
