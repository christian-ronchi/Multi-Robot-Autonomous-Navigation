import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # Declare the 'world' argument
    declare_world_arg = DeclareLaunchArgument(
        'world',
        # No default value here, we'll let gazebo_world.launch.py handle it
        # This makes it clear that the default is defined downstream.
        description='Full path to the world file to load.'
    )

    # Get the paths to the launch files for different components
    pkg_slam_multi_robot = get_package_share_directory('slam_multi_robot')
    pkg_merging_pkg = get_package_share_directory('merging_pkg')

    gazebo_launch = os.path.join(pkg_slam_multi_robot, 'launch', 'gazebo_world.launch.py')
    slam_launch = os.path.join(pkg_slam_multi_robot, 'launch', 'slam_bringup.launch.py')
    merge_maps_launch = os.path.join(pkg_merging_pkg, 'launch', 'map_merging.launch.py')
    navigation_launch = os.path.join(pkg_slam_multi_robot, 'launch', 'navigation.launch.py')
    transform_launch = os.path.join(pkg_slam_multi_robot, 'launch', 'static_transform.launch.py')
    filter_launch = os.path.join(pkg_merging_pkg, 'launch', 'laser_filters.launch.py')

    # Launch Gazebo simulation immediately
    # Pass the 'world' argument to the included launch file
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch),
        launch_arguments={'world': LaunchConfiguration('world')}.items()
    )

    # Launch static transforms after a 5-second delay to ensure Gazebo is up
    transform_launch = TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(transform_launch)
            )
        ]
    )

    # Launch laser filters after a 10-second delay
    filter_launch = TimerAction(
        period=10.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(filter_launch)
            )
        ]
    )

    # Launch SLAM for each robot after a 15-second delay
    tb_slam = TimerAction(
        period=15.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(slam_launch)
            )
        ]
    )

    # Launch the map merging node with the same delay as SLAM
    merge_maps = TimerAction(
        period=15.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(merge_maps_launch)
            )
        ]
    )
    
    # Launch the navigation stack for each robot after a 30-second delay
    navigation = TimerAction(
        period=30.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(navigation_launch)
            )
        ]
    )

    return LaunchDescription([
        declare_world_arg,
        gazebo,
        transform_launch,
        filter_launch,
        tb_slam,
        merge_maps,
        navigation
    ])
