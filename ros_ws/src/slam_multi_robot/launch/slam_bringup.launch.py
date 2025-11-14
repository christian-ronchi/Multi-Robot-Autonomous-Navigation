import os
import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode
from slam_scripts.utils import generate_namespaced_slam_params

def generate_launch_description():
    # Set up paths to configuration files
    pkg_slam_multi_robot = get_package_share_directory('slam_multi_robot')
    pkg_multi_robot_bringup = get_package_share_directory('multi_robot_bringup')
    robots_config_file = os.path.join(pkg_multi_robot_bringup, 'config', 'robots.yaml')
    params_template = os.path.join(pkg_slam_multi_robot, 'params', 'slam_params.yaml')
    
    # Load the robot configurations from the YAML file
    with open(robots_config_file, 'r') as file:
        robots_config = yaml.safe_load(file)
    
    # Filter for robots that are marked as enabled
    enabled_robots = [robot for robot in robots_config['robots'] if robot.get('enabled', True)]

    # Declare the 'use_sim_time' launch argument
    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_use_sim_time_argument = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time_argument)

    # Create and launch a SLAM node for each enabled robot
    for i, robot in enumerate(enabled_robots):
        robot_name = robot['name']
        
        slam_params_file =generate_namespaced_slam_params(params_template, robot_name)
        
        slam_node = LifecycleNode(
            parameters=[
                slam_params_file,
                {'use_sim_time': use_sim_time}
            ],
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name=f'slam_toolbox_{robot_name}',
            output='screen',
            namespace="",
            remappings=[('map', f'{robot_name}/map')],
            # autostart=True ensures the node automatically transitions
            # through the 'configuring' and 'activating' lifecycle states.
            autostart=True
        )

        # Stagger the launch of each SLAM node to prevent resource contention on startup
        delay_action = TimerAction(
            period=float(i) * 2.0,  # 2-second delay between each node
            actions=[slam_node]
        )
        
        ld.add_action(delay_action)

    return ld
