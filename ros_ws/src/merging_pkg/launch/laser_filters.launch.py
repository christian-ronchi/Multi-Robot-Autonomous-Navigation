import os
import yaml
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    ld = LaunchDescription()
    
    # Declare and get the 'use_sim_time' launch argument
    use_sim_time = LaunchConfiguration("use_sim_time", default="true")
    
    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time", 
        default_value="true",
        description="Use simulation (Gazebo) clock if true"
    )
    
    # Load robot configurations from the YAML file
    config_path = os.path.join(
        get_package_share_directory("multi_robot_bringup"),
        'config',
        'robots.yaml'
    )
    
    filter_nodes = []
    enabled_robots = []
    
    try:
        # Open and parse the robot configuration file
        with open(config_path, 'r') as file:
            config_data = yaml.safe_load(file)
        
        if 'robots' in config_data:
            for robot in config_data['robots']:
                if robot['enabled']:
                    # Create a laser filter node for each enabled robot
                    node = Node(
                        package="merging_pkg",
                        executable="robot_laser_filter",
                        name=f"{robot['name']}_laser_filter",
                        parameters=[{
                            'use_sim_time': use_sim_time,
                            'robot_name': robot['name'],
                            'robot_radius': 0.3,
                            'safety_margin': 0.2,
                            'filter_enabled': True
                        }],
                        output="screen"
                    )
                    filter_nodes.append(node) # Add the node to the list
                    enabled_robots.append(robot['name']) # Keep track of enabled robots
                    print(f"Added laser filter for robot: {robot['name']}")
                else:
                    print(f"Skipping disabled robot: {robot['name']} (not enabled in config)")
        
        print(f"Total laser filters: {len(filter_nodes)} for robots: {enabled_robots}")
    
    except Exception as e:
        print(f"Error loading robot configurations: {e}")
        print("Using default robot configurations as a fallback...")
        
        # Fallback to default robots if configuration loading fails
        default_robots = ['tb1', 'tb2']
        
        for robot_name in default_robots:
            node = Node(
                package="merging_pkg",
                executable="robot_laser_filter",
                name=f"{robot_name}_laser_filter",
                parameters=[{
                    'use_sim_time': use_sim_time,
                    'robot_name': robot_name,
                    'robot_radius': 0.3,
                    'safety_margin': 0.2,
                    'filter_enabled': True
                }],
                output="screen"
            )
            filter_nodes.append(node) # Add the node to the list
            enabled_robots.append(robot_name) # Keep track of enabled robots
    
    # Add the 'use_sim_time' argument declaration to the launch description
    ld.add_action(declare_use_sim_time)
    
    # Add all generated filter nodes to the launch description
    for filter_node in filter_nodes:
        ld.add_action(filter_node)
    
    return ld