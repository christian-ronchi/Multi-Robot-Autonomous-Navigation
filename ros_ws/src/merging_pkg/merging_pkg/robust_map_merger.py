#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
import numpy as np
from geometry_msgs.msg import TransformStamped, Point
import tf2_ros
import tf2_geometry_msgs
from threading import Lock
from rclpy.qos import QoSProfile, DurabilityPolicy, ReliabilityPolicy, HistoryPolicy
import yaml
from ament_index_python.packages import get_package_share_directory
import os
from std_srvs.srv import Trigger
import time

class RobustMapMerger(Node):
    def __init__(self):
        super().__init__('robust_map_merger')
        
        # Configurable parameters
        self.save_directory = self.declare_parameter(
            'save_directory', 
            os.path.join('src', 'multi_robot_bringup', 'map')
        ).value
        
        self.map_name = self.declare_parameter(
            'map_name', 
            'merged_map'
        ).value

        # Load robot configurations
        self.robot_configs = self.load_robot_configurations()
        
        # Load QoS for maps
        map_qos = QoSProfile(
            depth=10,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST
        )
        
        # Publishers and subscribers
        self.merged_pub = self.create_publisher(OccupancyGrid, '/map_merged', map_qos)
        
        # Create subscribers only for enabled robots
        self.map_subscribers = {}
        self.maps = {}
        
        for robot_name, config in self.robot_configs.items():
            if config['enabled']:
                self.maps[robot_name] = None
                topic_name = f'/{robot_name}/map'
                self.map_subscribers[robot_name] = self.create_subscription(
                    OccupancyGrid, 
                    topic_name, 
                    self.create_callback(robot_name), 
                    map_qos
                )
                self.get_logger().info(f"Subscribed to {topic_name} for robot {robot_name}")
        
        # TF buffer for transforms
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        
        self.map_lock = Lock()

        # Service to save the merged map
        self.save_map_service = self.create_service(
            Trigger, 
            'save_merged_map', 
            self.save_map_callback
        )
        
        # Last merged map
        self.last_merged_map = None
        
        # Merging parameters
        self.merge_timer = self.create_timer(2.0, self.merge_maps)
        
        self.get_logger().info(f"Robust Map Merger started for {len(self.maps)} enabled robots")
        self.get_logger().info(f"Save directory: {self.save_directory}")
        self.get_logger().info(f"Map name: {self.map_name}")
        self.get_logger().info("Usage:")
        self.get_logger().info("1. Change directory: ros2 param set /robust_map_merger save_directory '/path/to/directory'")
        self.get_logger().info("2. Change map name: ros2 param set /robust_map_merger map_name 'my_map'")
        self.get_logger().info("3. Save map: ros2 service call /save_merged_map std_srvs/srv/Trigger '{}'")
    
    def save_map_callback(self, request, response):
        """Callback for the map saving service"""
        try:
            if self.last_merged_map:
                # Get current parameters
                current_save_dir = self.get_parameter('save_directory').value
                current_map_name = self.get_parameter('map_name').value
                
                success = self.save_map_to_file(self.last_merged_map, current_save_dir, current_map_name)
                if success:
                    response.success = True
                    response.message = f"Map '{current_map_name}' saved successfully to {current_save_dir}"
                    self.get_logger().info(response.message)
                else:
                    response.success = False
                    response.message = "Failed to save map"
                    self.get_logger().error(response.message)
            else:
                response.success = False
                response.message = "No merged map available to save"
                self.get_logger().warn(response.message)
            
            return response
            
        except Exception as e:
            self.get_logger().error(f"Error saving map: {e}")
            response.success = False
            response.message = f"Error saving map: {str(e)}"
            return response
    
    def save_map_to_file(self, map_msg, save_directory, map_name="merged_map"):
        """Saves the map to a PGM and YAML file"""
        try:
            # Expand path if it contains ~
            save_directory = os.path.expanduser(save_directory)
            
            # Create directory if it doesn't exist
            os.makedirs(save_directory, exist_ok=True)
            
            # Save PGM file
            pgm_filename = os.path.join(save_directory, f"{map_name}.pgm")
            self.save_map_as_pgm(map_msg, pgm_filename)
            
            # Salva YAML file 
            yaml_filename = os.path.join(save_directory, f"{map_name}.yaml")
            self.save_map_as_yaml(map_msg, f"{map_name}.pgm", yaml_filename)
            
            self.get_logger().info(f"Map saved to: {yaml_filename}")
            return True
            
        except Exception as e:
            self.get_logger().error(f"Error saving map to file: {e}")
            return False
    
    def save_map_as_pgm(self, map_msg, filename):
        """Saves the map as a PGM file"""
        width = map_msg.info.width
        height = map_msg.info.height
        
        with open(filename, 'wb') as pgm_file:
            # Header PGM
            header = f"P5\n{width} {height}\n255\n"
            pgm_file.write(header.encode())

            # Map data
            # Iterate from top row (height-1) to bottom row (0) to match PGM format (origin top-left)
            for i in range(height - 1, -1, -1):
                for j in range(width):
                    idx = i * width + j
                    value = map_msg.data[idx]
                    
                    # Converts to PGM format
                    if value == -1:  # Unknown
                        pgm_value = 205  # Grey
                    elif value == 0:   # Free
                        pgm_value = 254  # White
                    elif value == 100: # Occupied
                        pgm_value = 0   # Black
                    else:              # Intermediate values
                        pgm_value = max(0, min(255, 255 - int(value * 2.55)))
                    
                    pgm_file.write(bytes([pgm_value]))
    
    def save_map_as_yaml(self, map_msg, pgm_filename, yaml_filename):
        """Saves the map metadata as a YAML file"""
        try:
            from tf_transformations import euler_from_quaternion
            
            orientation = map_msg.info.origin.orientation
            roll, pitch, yaw = euler_from_quaternion([orientation.x, orientation.y, orientation.z, orientation.w])
            
            yaml_data = {
                'image': pgm_filename,
                'resolution': float(map_msg.info.resolution),
                'origin': [
                    float(map_msg.info.origin.position.x),
                    float(map_msg.info.origin.position.y),
                    float(yaw)
                ],
                'negate': 0,
                'occupied_thresh': 0.65,
                'free_thresh': 0.25
            }
            
            with open(yaml_filename, 'w') as yaml_file:
                yaml.dump(yaml_data, yaml_file, default_flow_style=False)
                
        except ImportError:
            # Fallback if tf_transformations is not available
            yaml_data = {
                'image': pgm_filename,
                'resolution': float(map_msg.info.resolution),
                'origin': [
                    float(map_msg.info.origin.position.x),
                    float(map_msg.info.origin.position.y),
                    0.0
                ],
                'negate': 0,
                'occupied_thresh': 0.65,
                'free_thresh': 0.25
            }
            
            with open(yaml_filename, 'w') as yaml_file:
                yaml.dump(yaml_data, yaml_file, default_flow_style=False)
    
    def load_robot_configurations(self):
        """Loads robot configurations from the YAML file"""
        try:
            package_name = "multi_robot_bringup"
            config_path = os.path.join(
                get_package_share_directory(package_name),
                'config',
                'robots.yaml'
            )
            
            self.get_logger().info(f"Loading robot configurations from: {config_path}")
            
            with open(config_path, 'r') as file:
                config_data = yaml.safe_load(file)
            
            robot_configs = {}
            if 'robots' in config_data:
                for robot in config_data['robots']:
                    robot_name = robot['name']
                    robot_configs[robot_name] = {
                        'x_pose': float(robot['x_pose']),
                        'y_pose': float(robot['y_pose']),
                        'z_pose': float(robot['z_pose']),
                        'enabled': robot['enabled']
                    }
                    self.get_logger().info(f"Loaded config for {robot_name}: {robot_configs[robot_name]}")
            
            self.get_logger().info(f"Successfully loaded configurations for {len(robot_configs)} robots")
            return robot_configs
            
        except Exception as e:
            self.get_logger().error(f"Failed to load robot configurations: {e}")
            return self.get_default_configurations()
    
    def get_default_configurations(self):
        """Provides default robot configurations if YAML loading fails"""
        self.get_logger().warn("Using default robot configurations")
        return {
            'tb1': {'x_pose': 0.5, 'y_pose': -0.5, 'z_pose': 0.01, 'enabled': True},
            'tb2': {'x_pose': -1.5, 'y_pose': 0.5, 'z_pose': 0.01, 'enabled': True},
            'tb3': {'x_pose': -0.5, 'y_pose': -0.5, 'z_pose': 0.01, 'enabled': False},
            'tb4': {'x_pose': 1.5, 'y_pose': 0.5, 'z_pose': 0.01, 'enabled': False}
        }
    
    def create_callback(self, robot_name):
        """Creates a callback function for a specific robot"""
        def callback(msg):
            with self.map_lock:
                self.maps[robot_name] = msg
            self.get_logger().debug(f"Received map for {robot_name}")
        return callback
    
    def merge_maps(self):
        with self.map_lock:
            # Check if we have at least 1 map
            available_maps = {k: v for k, v in self.maps.items() if v is not None}
            if len(available_maps) < 1:
                self.get_logger().debug(f"Waiting for maps. Currently have: {list(available_maps.keys())}")
                return
            
            try:
                merged_map = self.create_merged_map_advanced(available_maps)
                if merged_map:
                    self.merged_pub.publish(merged_map)
                    self.last_merged_map = merged_map
                    self.get_logger().info(f"Successfully published merged map from {len(available_maps)} robots")
                
            except Exception as e:
                self.get_logger().error(f"Error merging maps: {e}")
    
    def create_merged_map_advanced(self, available_maps):
        """Advanced merging logic that properly combines all available maps"""
        
        # Get map transforms to global frame
        transforms = {}
        for robot_name in available_maps.keys():
            transform = self.get_map_transform(robot_name)
            if transform:
                transforms[robot_name] = transform
        
        if len(transforms) < 1:
            self.get_logger().warn("Could not get enough transforms, using fallback merge")
            return self.fallback_merge(available_maps)
        
        # Calculate merged map bounds
        bounds = self.calculate_merged_bounds(available_maps, transforms)
        
        # Create merged map
        merged_map = self.create_empty_merged_map(bounds)
        
        # Merge all maps into the merged frame
        for robot_name, map_msg in available_maps.items():
            if robot_name in transforms:
                self.merge_single_map(merged_map, map_msg, transforms[robot_name])
        
        return merged_map
    
    def get_map_transform(self, robot_name):
        """Get transform from robot's map frame to global map frame"""
        try:
            transform = self.tf_buffer.lookup_transform(
                'map', 
                f'{robot_name}/map', 
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=1.0)
            )
            return transform
        except Exception as e:
            self.get_logger().warn(f"Could not get transform for {robot_name}: {e}")
            # Fallback to initial pose from YAML
            return self.create_transform_from_yaml_pose(robot_name)
    
    def create_transform_from_yaml_pose(self, robot_name):
        """Create transform from YAML pose when TF is not available"""
        if robot_name in self.robot_configs:
            config = self.robot_configs[robot_name]
            transform = TransformStamped()
            transform.transform.translation.x = config['x_pose']
            transform.transform.translation.y = config['y_pose']
            transform.transform.translation.z = config['z_pose']
            transform.transform.rotation.w = 1.0
            return transform
        return None
    
    def calculate_merged_bounds(self, available_maps, transforms):
        """Calculate the bounds needed to contain all maps"""
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')
        
        for robot_name, map_msg in available_maps.items():
            if robot_name in transforms:
                # Calculate corners of this map in global frame
                corners = self.get_map_corners(map_msg, transforms[robot_name])
                
                for corner in corners:
                    min_x = min(min_x, corner.x)
                    min_y = min(min_y, corner.y)
                    max_x = max(max_x, corner.x)
                    max_y = max(max_y, corner.y)
        
        # If there were no transforms, use YAML poses
        if min_x == float('inf'):
            for robot_name, config in self.robot_configs.items():
                if config['enabled']:
                    min_x = min(min_x, config['x_pose'] - 5.0)
                    min_y = min(min_y, config['y_pose'] - 5.0)
                    max_x = max(max_x, config['x_pose'] + 5.0)
                    max_y = max(max_y, config['y_pose'] + 5.0)
        
        # Add padding
        padding = 0.5
        return {
            'min_x': min_x - padding,
            'min_y': min_y - padding,
            'max_x': max_x + padding,
            'max_y': max_y + padding
        }
    
    def get_map_corners(self, map_msg, transform):
        """Get the four corners of a map in global coordinates"""
        corners = []
        origin_x = map_msg.info.origin.position.x
        origin_y = map_msg.info.origin.position.y
        width = map_msg.info.width * map_msg.info.resolution
        height = map_msg.info.height * map_msg.info.resolution
        
        local_corners = [
            Point(x=origin_x, y=origin_y, z=0.0),
            Point(x=origin_x + width, y=origin_y, z=0.0),
            Point(x=origin_x + width, y=origin_y + height, z=0.0),
            Point(x=origin_x, y=origin_y + height, z=0.0)
        ]
        
        # Transform corners to global frame
        for corner in local_corners:
            global_corner = tf2_geometry_msgs.do_transform_point(
                tf2_geometry_msgs.PointStamped(point=corner), 
                transform
            )
            corners.append(global_corner.point)
        
        return corners
    
    def create_empty_merged_map(self, bounds):
        """Create an empty merged map with the specified bounds"""
        merged_map = OccupancyGrid()
        merged_map.header.stamp = self.get_clock().now().to_msg()
        merged_map.header.frame_id = "map"
        
        # Set resolution
        resolution = 0.05
        
        merged_map.info.resolution = resolution
        
        # Calculate dimensions
        width = int((bounds['max_x'] - bounds['min_x']) / resolution)
        height = int((bounds['max_y'] - bounds['min_y']) / resolution)
        
        # Ensure reasonable dimensions
        width = max(10, min(width, 10000))
        height = max(10, min(height, 10000))
        
        merged_map.info.width = width
        merged_map.info.height = height
        
        # Set origin
        merged_map.info.origin.position.x = bounds['min_x']
        merged_map.info.origin.position.y = bounds['min_y']
        merged_map.info.origin.position.z = 0.0
        merged_map.info.origin.orientation.w = 1.0
        
        # Initialize with unknown (-1)
        merged_map.data = [-1] * (width * height)
        
        return merged_map
    
    def merge_single_map(self, merged_map, source_map, transform):
        """Merge a single map into the merged map with free space priority (conservative version)"""
        resolution = merged_map.info.resolution
        merged_origin_x = merged_map.info.origin.position.x
        merged_origin_y = merged_map.info.origin.position.y
        
        source_resolution = source_map.info.resolution
        source_origin_x = source_map.info.origin.position.x
        source_origin_y = source_map.info.origin.position.y
        
        # For each cell in source map
        for y in range(source_map.info.height):
            for x in range(source_map.info.width):
                source_idx = y * source_map.info.width + x
                source_value = source_map.data[source_idx]
                
                if source_value == -1:
                    continue
                
                # Convert to world coordinates in source frame
                world_x = source_origin_x + (x + 0.5) * source_resolution
                world_y = source_origin_y + (y + 0.5) * source_resolution
                
                # Transform to global frame
                source_point = Point(x=world_x, y=world_y, z=0.0)
                global_point = tf2_geometry_msgs.do_transform_point(
                    tf2_geometry_msgs.PointStamped(point=source_point), 
                    transform
                )
                
                # Convert to merged map coordinates
                merged_x = int((global_point.point.x - merged_origin_x) / resolution)
                merged_y = int((global_point.point.y - merged_origin_y) / resolution)
                
                # Check bounds
                if (0 <= merged_x < merged_map.info.width and 
                    0 <= merged_y < merged_map.info.height):
                    
                    merged_idx = merged_y * merged_map.info.width + merged_x
                    
                    # CONSERVATIVE MERGING LOGIC: Free space has priority, but occupied needs confirmation
                    current_value = merged_map.data[merged_idx]
                    
                    if current_value == -1:
                        # Unknown cell - use source value
                        merged_map.data[merged_idx] = source_value
                    
                    elif source_value == 0:
                        # Source says free - always trust free space
                        merged_map.data[merged_idx] = 0
                    
                    elif source_value == 100 and current_value == 100:
                        # Only keep occupied if both current AND source agree it's occupied
                        merged_map.data[merged_idx] = 100
                    
                    elif source_value == 100 and current_value != 0 and current_value != 100:
                        # Source says occupied, current is not free and not already occupied
                        # You might want to set as occupied or use probabilistic value
                        merged_map.data[merged_idx] = 100
    
    def fallback_merge(self, available_maps):
        """Simple fallback merge when transforms aren't available"""
        self.get_logger().info("Using fallback merge")
        
        if available_maps:
            first_robot = list(available_maps.keys())[0]
            merged_map = OccupancyGrid()
            merged_map.header = available_maps[first_robot].header
            merged_map.info = available_maps[first_robot].info
            merged_map.data = available_maps[first_robot].data[:]
            
            return merged_map
        
        return None

def main():
    rclpy.init()
    node = RobustMapMerger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # On shutdown, save the last map if available
        if node.last_merged_map:
            node.get_logger().info("Saving map before shutdown...")
            save_dir = node.get_parameter('save_directory').value
            map_name = node.get_parameter('map_name').value
            node.save_map_to_file(node.last_merged_map, save_dir, f"{map_name}")
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()