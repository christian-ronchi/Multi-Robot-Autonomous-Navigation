import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point, PointStamped
import tf2_ros
import tf2_geometry_msgs
import math
from threading import Lock
import yaml
from ament_index_python.packages import get_package_share_directory
import os

class RobotLaserFilter(Node):
    def __init__(self):
        super().__init__('robot_laser_filter')
        
        # Parametri configurabili
        self.robot_name = self.declare_parameter('robot_name', 'tb1').value
        self.robot_radius = self.declare_parameter('robot_radius', 0.3).value
        self.safety_margin = self.declare_parameter('safety_margin', 0.2).value
        self.filter_enabled = self.declare_parameter('filter_enabled', True).value
        
        # Carica la lista degli altri robot dal file YAML
        self.other_robots = self.load_other_robots_config()
        
        # TF buffer per le trasformate
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        
        # Publisher e Subscriber
        self.filtered_scan_pub = self.create_publisher(
            LaserScan, 
            f'/{self.robot_name}/filtered_scan', 
            10
        )
        
        self.original_scan_sub = self.create_subscription(
            LaserScan,
            f'/{self.robot_name}/scan',
            self.scan_callback,
            10
        )
        
        self.lock = Lock()
        self.filtered_count = 0
        
        # Stati del filtro
        self.filter_state = "BOOTSTRAP"  # BOOTSTRAP → PARTIAL → FULL
        self.bootstrap_start_time = self.get_clock().now()
        self.bootstrap_duration = 10.0  # secondi
        
        # Timer per transizione di stato
        self.state_timer = self.create_timer(2.0, self.update_filter_state)
        
        self.get_logger().info(f"Robot filter started for {self.robot_name}")
        self.get_logger().info(f"Filtering other robots: {self.other_robots}")
        self.get_logger().info(f"Robot radius: {self.robot_radius}m + safety margin: {self.safety_margin}m")
        self.get_logger().info("Starting in BOOTSTRAP mode (no filtering)")
    
    def update_filter_state(self):
        """Updates the filter state based on TF availability and elapsed time"""
        current_time = self.get_clock().now()
        elapsed_time = (current_time - self.bootstrap_start_time).nanoseconds / 1e9
        
        # BOOTSTRAP → PARTIAL after half the bootstrap duration if self TF is available
        if self.filter_state == "BOOTSTRAP" and elapsed_time > self.bootstrap_duration / 2:
            if self.check_self_tf():
                self.filter_state = "PARTIAL"
                self.get_logger().info("Transitioning to PARTIAL mode (self-filtering only)")
        
        # PARTIAL → FULL if all TFs are available
        elif self.filter_state == "PARTIAL":
            if self.check_all_tf():
                self.filter_state = "FULL"
                self.get_logger().info("Transitioning to FULL mode (full robot filtering)")
        
        # FULL check
        elif self.filter_state == "FULL":
            if not self.check_all_tf():
                self.filter_state = "PARTIAL"
                self.get_logger().warn("Falling back to PARTIAL mode (some TF missing)")
    
    def check_self_tf(self):
        """Check if the robot's own TF is available"""
        try:
            self.tf_buffer.lookup_transform(
                'map', 
                f'{self.robot_name}/base_scan',
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=0.1)
            )
            return True
        except:
            return False
    
    def check_all_tf(self):
        """Check if all necessary TFs are available"""
        if not self.check_self_tf():
            return False
        
        # Check TF for all other robots
        for robot_name in self.other_robots:
            try:
                self.tf_buffer.lookup_transform(
                    'map', 
                    f'{robot_name}/base_footprint',
                    rclpy.time.Time(),
                    timeout=rclpy.duration.Duration(seconds=0.1)
                )
                return True
            except:
                continue
        return False
    
    def scan_callback(self, msg):
        """Main callback to process incoming laser scans"""
        if not self.filter_enabled:
            self.filtered_scan_pub.publish(msg)
            return
            
        try:
            with self.lock:
                if self.filter_state == "BOOTSTRAP":
                    # Phase 1: No filtering, just forwarding
                    filtered_scan = self.forward_scan(msg)
                
                elif self.filter_state == "PARTIAL":
                    # Phase 2: Filter only self (avoid self-reflection)
                    filtered_scan = self.filter_self_only(msg)
                
                else:  # FULL
                    # Phase 3: Full filtering
                    filtered_scan = self.filter_robot_points(msg)
                
                if filtered_scan:
                    self.filtered_scan_pub.publish(filtered_scan)
                    
        except Exception as e:
            self.get_logger().error(f"Error in scan callback: {e}")
            # Fallback: directly publish original scan
            self.filtered_scan_pub.publish(msg)
    
    def forward_scan(self, scan_msg):
        """Simply forwards the scan without filtering"""
        return scan_msg
    
    def filter_self_only(self, scan_msg):
        """Filters only points that are too close to the robot itself"""
        filtered_scan = LaserScan()
        filtered_scan.header = scan_msg.header
        filtered_scan.angle_min = scan_msg.angle_min
        filtered_scan.angle_max = scan_msg.angle_max
        filtered_scan.angle_increment = scan_msg.angle_increment
        filtered_scan.time_increment = scan_msg.time_increment
        filtered_scan.scan_time = scan_msg.scan_time
        filtered_scan.range_min = scan_msg.range_min
        filtered_scan.range_max = scan_msg.range_max
        
        filtered_scan.ranges = list(scan_msg.ranges)
        filtered_scan.intensities = list(scan_msg.intensities) if scan_msg.intensities else []
        
        # Filters only points that are too close (likely self-reflection)
        min_valid_distance = self.robot_radius + 0.1  # 10cm beyond the robot's radius
        
        filtered_points = 0
        for i, range_val in enumerate(scan_msg.ranges):
            if (range_val < min_valid_distance and 
                range_val >= scan_msg.range_min and 
                not math.isinf(range_val) and 
                not math.isnan(range_val)):
                
                filtered_scan.ranges[i] = float('inf')
                if filtered_scan.intensities:
                    filtered_scan.intensities[i] = 0.0
                filtered_points += 1
        
        if filtered_points > 0 and self.filtered_count % 100 == 0:
            self.get_logger().info(f"Filtered {filtered_points} self-reflection points")
        
        return filtered_scan
    
    def filter_robot_points(self, scan_msg):
        """Filters laser points that hit other robots (full version)"""
        try:
            filtered_scan = LaserScan()
            filtered_scan.header = scan_msg.header
            filtered_scan.angle_min = scan_msg.angle_min
            filtered_scan.angle_max = scan_msg.angle_max
            filtered_scan.angle_increment = scan_msg.angle_increment
            filtered_scan.time_increment = scan_msg.time_increment
            filtered_scan.scan_time = scan_msg.scan_time
            filtered_scan.range_min = scan_msg.range_min
            filtered_scan.range_max = scan_msg.range_max
            
            filtered_scan.ranges = list(scan_msg.ranges)
            filtered_scan.intensities = list(scan_msg.intensities) if scan_msg.intensities else []
            
            robot_positions = self.get_other_robots_positions()
            if not robot_positions:
                return filtered_scan  # Returns scan with only self-filter
            
            filtered_points = 0
            
            for i, range_val in enumerate(scan_msg.ranges):
                if (range_val < scan_msg.range_min or 
                    range_val > scan_msg.range_max or 
                    math.isinf(range_val) or 
                    math.isnan(range_val)):
                    continue
                
                angle = scan_msg.angle_min + i * scan_msg.angle_increment
                point_in_laser = Point()
                point_in_laser.x = range_val * math.cos(angle)
                point_in_laser.y = range_val * math.sin(angle)
                point_in_laser.z = 0.0
                
                point_in_map = self.transform_point_to_map(point_in_laser, scan_msg.header)
                if not point_in_map:
                    continue
                
                if self.is_point_inside_robot(point_in_map, robot_positions):
                    filtered_scan.ranges[i] = float('inf')
                    if filtered_scan.intensities:
                        filtered_scan.intensities[i] = 0.0
                    filtered_points += 1
            
            if filtered_points > 0:
                self.filtered_count += filtered_points
                if self.filtered_count % 50 == 0:
                    self.get_logger().info(f"Filtered {filtered_points} robot points (total: {self.filtered_count})")
            
            return filtered_scan
            
        except Exception as e:
            self.get_logger().error(f"Error in full filtering: {e}")
            return self.filter_self_only(scan_msg)  # Fallback to partial filter


    
    def load_other_robots_config(self):
        """Loads the list of other robots from the YAML file"""
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
            
            other_robots = []
            if 'robots' in config_data:
                for robot in config_data['robots']:
                    if robot['name'] != self.robot_name and robot['enabled']:
                        other_robots.append(robot['name'])
                        self.get_logger().info(f"Will filter robot: {robot['name']}")
                    elif robot['name'] == self.robot_name:
                        self.get_logger().info(f"This robot: {robot['name']}")
                    elif not robot['enabled']:
                        self.get_logger().info(f"Skipping disabled robot: {robot['name']}")
            
            self.get_logger().info(f"Total robots to filter: {len(other_robots)}: {other_robots}")
            return other_robots
            
        except Exception as e:
            self.get_logger().error(f"Failed to load robot configurations: {e}")
            all_robots = ['tb1', 'tb2', 'tb3', 'tb4']
            other_robots = [r for r in all_robots if r != self.robot_name]
            self.get_logger().warn(f"Using fallback configuration: {other_robots}")
            return other_robots

    def get_other_robots_positions(self):
        """Gets the positions of all other robots in the map frame"""
        robot_positions = {}
        
        for robot_name in self.other_robots:
            try:
                pose = self.get_robot_pose(robot_name, 'base_footprint')
                if not pose:
                    pose = self.get_robot_pose(robot_name, 'base_link')
                
                if pose:
                    robot_positions[robot_name] = pose
                    
            except Exception as e:
                self.get_logger().debug(f"Could not get position for {robot_name}: {e}")
                continue
        
        return robot_positions

    def get_robot_pose(self, robot_name, frame_suffix):
        """Gets the position of a specific robot"""
        try:
            transform = self.tf_buffer.lookup_transform(
                'map',
                f'{robot_name}/{frame_suffix}',
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=0.5)
            )
            
            pose = Point()
            pose.x = transform.transform.translation.x
            pose.y = transform.transform.translation.y
            pose.z = transform.transform.translation.z
            
            return pose
            
        except:
            return None

    def transform_point_to_map(self, point, header):
        """Transforms a point from the laser frame to the map frame"""
        try:
            point_stamped = PointStamped()
            point_stamped.header = header
            point_stamped.point = point
            
            transform = self.tf_buffer.lookup_transform(
                'map',
                header.frame_id,
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=0.5)
            )
            
            point_in_map = tf2_geometry_msgs.do_transform_point(point_stamped, transform)
            return point_in_map.point
            
        except:
            return None

    def is_point_inside_robot(self, point, robot_positions):
        """Checks if a point is inside the radius of another robot"""
        for robot_name, robot_pose in robot_positions.items():
            distance = math.sqrt(
                (point.x - robot_pose.x)**2 + 
                (point.y - robot_pose.y)**2
            )
            
            if distance < (self.robot_radius + self.safety_margin):
                return True
        
        return False

def main():
    rclpy.init()
    node = RobotLaserFilter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down robot filter...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()