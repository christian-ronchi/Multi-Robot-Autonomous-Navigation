import os
import yaml
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import ExecuteProcess
import subprocess

def generate_launch_description():
    
    # Declare a launch argument for the robot configuration file path
    config_path_arg = DeclareLaunchArgument(
        'config_file',
            default_value=os.path.join(
                get_package_share_directory('multi_robot_bringup'),
                'config',
                'robots.yaml'
            ),
        description='Path to the robots configuration YAML file'
    )
    
    launch_description = LaunchDescription()
    launch_description.add_action(config_path_arg)
    
    # Resolve the actual path to the robot configuration file
    # This uses a hardcoded path for now, but could be improved to use LaunchConfiguration('config_file')
    # if the config_file argument was intended to be dynamic.
    pkg_slam_multi_robot = get_package_share_directory('slam_multi_robot')
    pkg_multi_robot_bringup = get_package_share_directory('multi_robot_bringup')
    actual_config_path = os.path.join(pkg_multi_robot_bringup, 'config', 'robots.yaml')
    
    try:
        with open(actual_config_path, 'r') as file:
            config_data = yaml.safe_load(file)
        
        # Iterate through all robots defined in the configuration file
        for robot in config_data['robots']:
            # Check if the robot is enabled
            if robot.get('enabled', False):
                # Create a static transform publisher for the enabled robot
                # This connects the robot's local map frame to the global 'map' frame.
                static_transform_node = Node(
                    package='tf2_ros',
                    executable='static_transform_publisher',
                    name=f'static_transform_publisher_{robot["name"]}',
                    arguments=[
                        str(robot['x_pose']),
                        str(robot['y_pose']), 
                        str(robot['z_pose']),
                        '0', '0', '0',  # yaw, pitch, roll
                        'map',
                        f'{robot["name"]}/map'
                    ],
                    output='screen'
                )
                launch_description.add_action(static_transform_node)
                
    except Exception as e:
        # Log an error if the configuration file cannot be read
        print(f"Error reading robot configuration file: {e}")
    
    return launch_description