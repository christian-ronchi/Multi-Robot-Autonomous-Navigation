import os
import yaml
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    ld = LaunchDescription()
    
    use_sim_time = LaunchConfiguration("use_sim_time", default="true")
    
    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time", 
        default_value="true",
        description="Use simulation clock"
    )
    
    # Custom map merger node
    map_merger_node = Node(
        package="merging_pkg",
        executable="merger_node",
        name="robust_map_merger",
        parameters=[{"use_sim_time": use_sim_time}],
        output="screen",
        emulate_tty=True
    )
    
    ld.add_action(declare_use_sim_time)
    ld.add_action(map_merger_node)
    
    return ld