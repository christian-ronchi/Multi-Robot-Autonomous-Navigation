#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from rclpy.qos import qos_profile_sensor_data, QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from sensor_msgs.msg import LaserScan, PointCloud2, PointField
from std_msgs.msg import Header
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point, PointStamped, Vector3
from dynamic_obstacle_detector_interfaces.msg import TrackedObject, TrackedObjectArray
import struct
import numpy as np
from sklearn.cluster import DBSCAN
from scipy.optimize import linear_sum_assignment
import threading
from rclpy.parameter import Parameter
import tf2_ros
from tf2_ros import TransformException
import tf2_geometry_msgs
from rcl_interfaces.msg import SetParametersResult
from typing import List, Tuple, Dict, Any, Optional
import math
from scipy.spatial.distance import mahalanobis


def stamp_to_secs(stamp) -> float:
    """Convert builtin time (msg stamp) to float seconds"""
    return float(stamp.sec) + float(stamp.nanosec) * 1e-9


class TrackedObstacle:
    """Enhanced tracked obstacle with better handling for dynamic obstacles near robot"""

    def __init__(self, obstacle_id: int, initial_cluster_cartesian: List[Tuple[float, float]], 
                 timestamp, kf_params: Dict[str, List[float]], logger):
        self.id = obstacle_id
        self.current_cartesian_cluster = []
        self.last_timestamp = timestamp
        self.logger = logger
        self.consecutive_misses = 0
        self.consecutive_detections = 0
        self.stable_track = False
        self.last_measurement = None

        # Kalman Filter Initialization with more conservative parameters
        initial_center = np.mean(np.array(initial_cluster_cartesian), axis=0)[:2]
        self.X = np.array([initial_center[0], initial_center[1], 0.0, 0.0], dtype=float).reshape(4, 1)

        # Higher initial uncertainty for velocity
        self.P = np.diag(kf_params['p']).astype(float)
        
        # Constant-velocity model
        self.F = np.eye(4, dtype=float)
        self.H = np.array([[1.0, 0.0, 0.0, 0.0],
                          [0.0, 1.0, 0.0, 0.0]], dtype=float)
        self.R = np.diag(kf_params['r']).astype(float)
        self.Q = np.diag(kf_params['q']).astype(float)

    def update(self, Z: np.ndarray, timestamp, measurement_quality: float = 1.0):
        """Enhanced update with measurement quality weighting"""
        dt = (timestamp.sec - self.last_timestamp.sec) + (timestamp.nanosec - self.last_timestamp.nanosec) * 1e-9
        
        if dt < 0.0:
            self.logger.warning(f"Negative dt in update for track {self.id}: {dt}. Skipping update.")
            return

        self.last_timestamp = timestamp
        self.last_measurement = Z.copy()
        
        # Adaptive measurement noise based on quality
        R_adaptive = self.R * (1.0 / max(0.1, measurement_quality))

        # Innovation
        y = Z - (self.H @ self.X)

        # Innovation covariance
        S = self.H @ self.P @ self.H.T + R_adaptive

        try:
            PHt = self.P @ self.H.T
            K = (np.linalg.solve(S, PHt.T)).T
        except np.linalg.LinAlgError:
            self.logger.warning(f"Singular innovation covariance S for track {self.id}; skipping correction.")
            return

        # Update state & covariance
        self.X = self.X + K @ y
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ self.H) @ self.P

        # Track stability metrics
        self.consecutive_misses = 0
        self.consecutive_detections += 1
        if self.consecutive_detections > 3:  # Require multiple detections for stable track
            self.stable_track = True

    def predict(self, dt: float):
        """Predict with adaptive process noise based on track stability"""
        if dt <= 0.0:
            return
            
        # Increase process noise for unstable tracks
        Q_adaptive = self.Q
        if not self.stable_track:
            Q_adaptive = self.Q * 2.0  # Higher uncertainty for new tracks

        self.F = np.array([[1.0, 0.0, dt, 0.0],
                          [0.0, 1.0, 0.0, dt],
                          [0.0, 0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0, 1.0]], dtype=float)
        self.X = self.F @ self.X
        self.P = self.F @ self.P @ self.F.T + Q_adaptive

    def mark_missed(self):
        """Mark that this track was not detected in current frame"""
        self.consecutive_misses += 1
        self.consecutive_detections = max(0, self.consecutive_detections - 1)

    def get_center(self) -> Tuple[float, float]:
        return (float(self.X[0, 0]), float(self.X[1, 0]))

    def get_velocity(self) -> Tuple[float, float]:
        return (float(self.X[2, 0]), float(self.X[3, 0]))

    def get_velocity_magnitude(self) -> float:
        vx, vy = self.get_velocity()
        return math.sqrt(vx*vx + vy*vy)

    def get_last_seen_time(self):
        return self.last_timestamp

    def get_covariance(self) -> np.ndarray:
        return self.P

    def is_reliable(self) -> bool:
        """Check if track is reliable enough for predictions"""
        return self.stable_track and self.consecutive_misses <= 2


class ObstacleDetectorNode(Node):
    def __init__(self):
        super().__init__('obstacle_detector_node')

        # Thread lock for tracks
        self._tracks_lock = threading.RLock()  # Changed to RLock for better nesting

        # Node state
        self.tracked_obstacles: Dict[int, TrackedObstacle] = {}
        self.next_obstacle_id = 0
        self.last_scan_time = None

        # TF buffer/listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Declare and load parameters
        self.declare_all_parameters()
        self.read_all_parameters()

        # Subscriptions & publishers
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            qos_profile_sensor_data)

        # Use reliable for markers, best effort for high-frequency data
        pub_qos = QoSProfile(
            depth=10, 
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            durability=DurabilityPolicy.VOLATILE
        )
        
        self.obstacle_pub = self.create_publisher(PointCloud2, 'predicted_obstacles', pub_qos)
        self.cluster_pub = self.create_publisher(PointCloud2, 'detected_obstacles', pub_qos)
        self.marker_pub = self.create_publisher(MarkerArray, 'velocity_markers', pub_qos)

        # Tracked objects for costmap layers often need to be reliable
        tracked_objects_qos = QoSProfile(
            depth=10, reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST, durability=DurabilityPolicy.VOLATILE
        )
        self.tracked_obstacles_pub = self.create_publisher(TrackedObjectArray, 'tracked_obstacles', tracked_objects_qos)

        # Dynamic parameter callback
        self.add_on_set_parameters_callback(self.parameters_callback)

        self.get_logger().info('Enhanced obstacle detection node started.')

    def declare_all_parameters(self):
        """Declare all parameters with better defaults for dynamic obstacles"""
        # Tracking and Prediction parameters
        self.declare_parameter('mahalanobis_gate', 6.0)  # Reduced from 9.21 for stricter association
        self.declare_parameter('track_lifetime', 1.5)    # Reduced lifetime for dynamic environments
        self.declare_parameter('prediction_horizon', 3.0) # Reduced horizon for stability
        self.declare_parameter('prediction_steps', 10)
        self.declare_parameter('target_frame', 'odom')
        self.declare_parameter('robot_id', '')
        
        # Enhanced KF parameters for dynamic obstacles
        self.declare_parameter('kf.p', [0.2, 0.2, 5.0, 5.0])  # Higher position uncertainty
        self.declare_parameter('kf.r', [0.5, 0.5])           # Higher measurement noise
        self.declare_parameter('kf.q', [0.01, 0.01, 0.1, 0.1]) # Higher process noise
        
        # DBSCAN clustering parameters optimized for dynamic obstacles
        self.declare_parameter('dbscan_eps', 0.4)
        self.declare_parameter('dbscan_min_samples', 3)      # Lower for better detection
        
        # New parameters for dynamic obstacle handling
        self.declare_parameter('transform_timeout_sec', 0.1)
        self.declare_parameter('min_obstacle_distance', 0.2)  # Increased minimum distance
        self.declare_parameter('max_obstacle_distance', 10.0)
        self.declare_parameter('min_velocity_for_prediction', 0.1)  # Only predict moving obstacles
        self.declare_parameter('cluster_quality_threshold', 0.7)   # Minimum cluster quality

    def parameters_callback(self, params):
        """Handle dynamic parameter changes"""
        try:
            self.read_all_parameters()
            return SetParametersResult(successful=True)
        except Exception as e:
            self.get_logger().error(f"Failed to apply parameters: {e}")
            return SetParametersResult(successful=False, reason=str(e))

    def read_all_parameters(self):
        """Read and validate all parameters"""
        self.get_logger().debug("Loading parameters for obstacle_detector_node...")

        # Read basic parameters
        self.MAHALANOBIS_GATE = float(self.get_parameter('mahalanobis_gate').value)
        self.TRACK_LIFETIME = float(self.get_parameter('track_lifetime').value)
        self.PREDICTION_HORIZON = float(self.get_parameter('prediction_horizon').value)
        self.PREDICTION_STEPS = int(self.get_parameter('prediction_steps').value)
        self.TARGET_FRAME = str(self.get_parameter('target_frame').value)
        self.robot_id = str(self.get_parameter('robot_id').value) or ''
        self.DBSCAN_EPS = float(self.get_parameter('dbscan_eps').value)
        self.DBSCAN_MIN_SAMPLES = int(self.get_parameter('dbscan_min_samples').value)
        self.TRANSFORM_TIMEOUT = float(self.get_parameter('transform_timeout_sec').value)
        self.MIN_OBSTACLE_DISTANCE = float(self.get_parameter('min_obstacle_distance').value)
        self.MAX_OBSTACLE_DISTANCE = float(self.get_parameter('max_obstacle_distance').value)
        self.MIN_VELOCITY_FOR_PREDICTION = float(self.get_parameter('min_velocity_for_prediction').value)
        self.CLUSTER_QUALITY_THRESHOLD = float(self.get_parameter('cluster_quality_threshold').value)

        # KF params with validation - CORREZIONE APPLICATA
        kf_p = self.get_parameter('kf.p').value
        kf_r = self.get_parameter('kf.r').value
        kf_q = self.get_parameter('kf.q').value
        
        # Correzione: rimossa parentesi extra e migliorata la leggibilità
        if not isinstance(kf_p, (list, tuple)) or len(kf_p) != 4:
            self.get_logger().warning('kf.p must be a list of 4 numbers. Using defaults.')
            kf_p = [0.2, 0.2, 5.0, 5.0]
        
        if not isinstance(kf_r, (list, tuple)) or len(kf_r) != 2:
            self.get_logger().warning('kf.r must be a list of 2 numbers. Using defaults.')
            kf_r = [0.5, 0.5]
        
        if not isinstance(kf_q, (list, tuple)) or len(kf_q) != 4:
            self.get_logger().warning('kf.q must be a list of 4 numbers. Using defaults.')
            kf_q = [0.01, 0.01, 0.1, 0.1]
            
        self.kf_params = {'p': kf_p, 'r': kf_r, 'q': kf_q}

        # Validate other parameters
        if self.MAHALANOBIS_GATE <= 0:
            self.get_logger().warning('mahalanobis_gate must be > 0. Setting to 6.0')
            self.MAHALANOBIS_GATE = 6.0
            
        if self.DBSCAN_EPS <= 0:
            self.get_logger().warning('dbscan_eps must be > 0. Setting to 0.4')
            self.DBSCAN_EPS = 0.4
            
        if self.DBSCAN_MIN_SAMPLES < 1:
            self.get_logger().warning('dbscan_min_samples must be >= 1. Setting to 3')
            self.DBSCAN_MIN_SAMPLES = 3
            
        if self.MIN_OBSTACLE_DISTANCE < 0:
            self.get_logger().warning('min_obstacle_distance must be >= 0. Setting to 0.2')
            self.MIN_OBSTACLE_DISTANCE = 0.2

    def scan_callback(self, msg: LaserScan):
        """Enhanced scan callback with better error handling"""
        # Rate limiting
        current_time = stamp_to_secs(msg.header.stamp)
        if self.last_scan_time and (current_time - self.last_scan_time) < 0.05:  # 20Hz max
            return
        self.last_scan_time = current_time

        try:
            # Lookup transform with better error handling
            transform = self.tf_buffer.lookup_transform(
                self.TARGET_FRAME,
                msg.header.frame_id,
                msg.header.stamp,
                timeout=Duration(seconds=self.TRANSFORM_TIMEOUT))
        except TransformException as ex:
            self.get_logger().warning(f'Transform error: {ex}')
            return

        # Convert scan with distance filtering
        points_in_laser_frame = self.convert_scan_to_cartesian(msg)
        if len(points_in_laser_frame) < 3:
            self.get_logger().debug("Not enough valid points in laser scan.")
            self.update_tracks_and_publish([], msg.header)
            return

        # Clustering with quality assessment
        clusters_in_laser_frame, cluster_qualities = self.cluster_points_with_quality(points_in_laser_frame)
        
        if not clusters_in_laser_frame:
            self.update_tracks_and_publish([], msg.header)
            return

        # Publish clusters for debugging
        self.publish_clusters_as_pointcloud(clusters_in_laser_frame, msg.header)

        # Compute cluster centroids with quality filtering
        cluster_centers_laser = []
        valid_cluster_qualities = []
        
        for i, cluster in enumerate(clusters_in_laser_frame):
            if cluster and cluster_qualities[i] >= self.CLUSTER_QUALITY_THRESHOLD:
                centroid = np.mean(np.array(cluster), axis=0)
                cluster_centers_laser.append((float(centroid[0]), float(centroid[1])))
                valid_cluster_qualities.append(cluster_qualities[i])

        # Transform to target frame
        cluster_centers_odom = self.transform_points(cluster_centers_laser, transform)

        # Update tracks with quality information
        self.update_tracks_and_publish(cluster_centers_odom, valid_cluster_qualities, msg.header)

    def cluster_points_with_quality(self, points: List[Tuple[float, float]]) -> Tuple[List[List[Tuple[float, float]]], List[float]]:
        """Enhanced clustering with quality metrics for each cluster"""
        if len(points) < 3:
            return [], []
            
        points_np = np.array(points, dtype=float)
        
        try:
            db = DBSCAN(eps=self.DBSCAN_EPS, min_samples=self.DBSCAN_MIN_SAMPLES)
            labels = db.fit_predict(points_np)
        except Exception as e:
            self.get_logger().warning(f'DBSCAN clustering failed: {e}')
            return [], []

        clusters = []
        qualities = []
        
        for k in set(labels):
            if k == -1:  # Noise
                continue
                
            mask = (labels == k)
            cluster_points = points_np[mask]
            clusters.append(cluster_points.tolist())
            
            # Calculate cluster quality based on density and size
            quality = self.calculate_cluster_quality(cluster_points)
            qualities.append(quality)

        return clusters, qualities

    def calculate_cluster_quality(self, cluster_points: np.ndarray) -> float:
        """Calculate quality metric for a cluster (0.0 to 1.0)"""
        if len(cluster_points) < 2:
            return 0.0
            
        # 1. Density quality (points per area)
        from scipy.spatial import ConvexHull
        try:
            if len(cluster_points) >= 3:
                hull = ConvexHull(cluster_points)
                area = hull.volume  # For 2D, volume is area
                density_quality = min(1.0, len(cluster_points) / (area + 1e-5) * 0.1)
            else:
                # For 2 points, use distance-based density
                distance = np.linalg.norm(cluster_points[0] - cluster_points[1])
                density_quality = min(1.0, 2.0 / (distance + 1e-5))
        except:
            density_quality = 0.5

        # 2. Size quality (not too small, not too large)
        cluster_size = np.std(cluster_points, axis=0).mean()
        size_quality = 1.0 - min(1.0, abs(cluster_size - 0.5) / 2.0)  # Prefer medium-sized clusters

        # 3. Compactness quality (how tightly packed)
        centroid = np.mean(cluster_points, axis=0)
        distances = np.linalg.norm(cluster_points - centroid, axis=1)
        compactness_quality = 1.0 - min(1.0, np.std(distances) / 0.5)

        return (density_quality + size_quality + compactness_quality) / 3.0

    def update_tracks_and_publish(self, cluster_centers_odom: List[Tuple[float, float]], 
                                cluster_qualities: List[float], header: Header):
        """Enhanced tracking pipeline with quality-aware updates"""
        output_header = Header(stamp=header.stamp, frame_id=self.TARGET_FRAME)

        # 1. Predict all tracks to current timestamp
        self._predict_all_tracks(header.stamp)

        # 2. Associate and update with quality weighting
        with self._tracks_lock:
            unmatched_cluster_indices, matched_track_ids = self._associate_and_update(
                cluster_centers_odom, cluster_qualities, header)

        # 3. Manage track lifecycle
        removed_track_ids = self._manage_track_lifecycle(
            unmatched_cluster_indices, matched_track_ids, 
            cluster_centers_odom, cluster_qualities, header)

        # 4. Prepare & publish messages
        self._prepare_and_publish_messages(output_header, removed_track_ids)

    def _associate_and_update(self, cluster_centers_odom: List[Tuple[float, float]],
                            cluster_qualities: List[float], header: Header):
        """Enhanced association with quality-based matching"""
        matched_track_ids = set()
        unmatched_cluster_indices = set(range(len(cluster_centers_odom)))

        if not self.tracked_obstacles or not cluster_centers_odom:
            return list(unmatched_cluster_indices), matched_track_ids

        track_ids = list(self.tracked_obstacles.keys())
        n_tracks = len(track_ids)
        n_clusters = len(cluster_centers_odom)

        LARGE_COST = 1e6
        cost_matrix = np.full((n_tracks, n_clusters), LARGE_COST, dtype=float)

        for i, tid in enumerate(track_ids):
            track = self.tracked_obstacles[tid]
            for j, cluster_center in enumerate(cluster_centers_odom):
                Z = np.array(cluster_center[:2]).reshape(2, 1)
                y = Z - (track.H @ track.X)
                S = track.H @ track.P @ track.H.T + track.R
                
                try:
                    sol = np.linalg.solve(S, y)
                    mahal_sq = float((y.T @ sol)[0, 0])
                    
                    # Apply quality-based gating
                    quality = cluster_qualities[j] if j < len(cluster_qualities) else 1.0
                    effective_gate = self.MAHALANOBIS_GATE * quality
                    
                    if mahal_sq < effective_gate:
                        cost_matrix[i, j] = mahal_sq
                except np.linalg.LinAlgError:
                    continue

        try:
            track_idx_arr, cluster_idx_arr = linear_sum_assignment(cost_matrix)
        except Exception as e:
            self.get_logger().warning(f'Assignment failed: {e}')
            return list(unmatched_cluster_indices), matched_track_ids

        # Process matches
        for t_idx, c_idx in zip(track_idx_arr, cluster_idx_arr):
            if cost_matrix[t_idx, c_idx] < LARGE_COST:
                tid = track_ids[t_idx]
                Z = np.array(cluster_centers_odom[c_idx][:2]).reshape(2, 1)
                quality = cluster_qualities[c_idx] if c_idx < len(cluster_qualities) else 1.0
                
                try:
                    self.tracked_obstacles[tid].update(Z, header.stamp, quality)
                    matched_track_ids.add(tid)
                    unmatched_cluster_indices.discard(c_idx)
                except Exception as e:
                    self.get_logger().warning(f"Track update failed: {e}")

        return list(unmatched_cluster_indices), matched_track_ids

    def _manage_track_lifecycle(self, unmatched_cluster_indices: List[int], 
                              matched_track_ids: set, cluster_centers_odom: List[Tuple[float, float]],
                              cluster_qualities: List[float], header: Header):
        """Enhanced lifecycle management"""
        current_time_sec = stamp_to_secs(header.stamp)
        tracks_to_remove = []

        with self._tracks_lock:
            # Mark missed detections and remove stale tracks
            for tid, track in list(self.tracked_obstacles.items()):
                if tid not in matched_track_ids:
                    track.mark_missed()
                    last_seen_sec = stamp_to_secs(track.get_last_seen_time())
                    if (current_time_sec - last_seen_sec) > self.TRACK_LIFETIME:
                        tracks_to_remove.append(tid)
                else:
                    # Reset missed counter for matched tracks
                    track.consecutive_misses = 0

            # Remove stale tracks
            for tid in tracks_to_remove:
                del self.tracked_obstacles[tid]

            # Create new tracks only for high-quality clusters
            for idx in unmatched_cluster_indices:
                if idx < len(cluster_qualities) and cluster_qualities[idx] >= self.CLUSTER_QUALITY_THRESHOLD:
                    try:
                        new_id = self.next_obstacle_id
                        self.tracked_obstacles[new_id] = TrackedObstacle(
                            new_id, [cluster_centers_odom[idx]], header.stamp, 
                            self.kf_params, self.get_logger())
                        self.next_obstacle_id += 1
                    except Exception as e:
                        self.get_logger().warning(f"Track creation failed: {e}")

        return tracks_to_remove

    def _prepare_and_publish_messages(self, header: Header, removed_track_ids: List[int]):
        """Enhanced message preparation with velocity-based prediction filtering"""
        marker_array = MarkerArray()

        # Remove markers for deleted tracks
        for tid in removed_track_ids:
            delete_marker = Marker()
            delete_marker.header = header
            delete_marker.ns = "velocity_vectors"
            delete_marker.id = tid
            delete_marker.action = Marker.DELETE
            marker_array.markers.append(delete_marker)

        all_prediction_points: List[Tuple[float, float, float]] = []
        tracked_objects_list: List[TrackedObject] = []

        with self._tracks_lock:
            for tid, track in self.tracked_obstacles.items():
                pos = track.get_center()
                vel = track.get_velocity()
                vel_mag = track.get_velocity_magnitude()

                # Only predict for reliable, moving tracks
                if track.is_reliable() and vel_mag >= self.MIN_VELOCITY_FOR_PREDICTION:
                    dt_step = self.PREDICTION_HORIZON / max(1, self.PREDICTION_STEPS)
                    for i in range(1, self.PREDICTION_STEPS + 1):
                        t = i * dt_step
                        pred_x = pos[0] + vel[0] * t
                        pred_y = pos[1] + vel[1] * t
                        all_prediction_points.append((pred_x, pred_y, 0.0))

                # Create velocity marker only for reliable tracks
                if track.is_reliable():
                    marker = Marker()
                    marker.header = header
                    marker.ns = "velocity_vectors"
                    marker.id = tid
                    marker.type = Marker.ARROW
                    marker.action = Marker.ADD
                    start_point = Point(x=pos[0], y=pos[1], z=0.0)
                    end_point = Point(x=pos[0] + vel[0], y=pos[1] + vel[1], z=0.0)
                    marker.points = [start_point, end_point]
                    marker.scale.x = 0.05
                    marker.scale.y = 0.1
                    marker.scale.z = 0.01
                    marker.color.a = 1.0
                    marker.color.r = 0.0
                    marker.color.g = 1.0
                    marker.color.b = 0.0
                    marker_array.markers.append(marker)

                # Always publish tracked object for costmap
                tobj = TrackedObject()
                tobj.id = int(tid)
                tobj.position.x = pos[0]
                tobj.position.y = pos[1]
                tobj.position.z = 0.0
                tobj.velocity.x = vel[0]
                tobj.velocity.y = vel[1]
                tobj.velocity.z = 0.0
                cov = track.get_covariance()
                tobj.covariance = cov.flatten().tolist()
                tracked_objects_list.append(tobj)

        # Publish all messages
        try:
            self.marker_pub.publish(marker_array)
            tracked_array_msg = TrackedObjectArray(header=header, objects=tracked_objects_list)
            self.tracked_obstacles_pub.publish(tracked_array_msg)
            
            if all_prediction_points:
                self._publish_prediction_pointcloud(all_prediction_points, header)
        except Exception as e:
            self.get_logger().error(f"Publishing failed: {e}")

    # Keep other methods similar but with enhanced error handling...
    def convert_scan_to_cartesian(self, scan_msg: LaserScan) -> List[Tuple[float, float]]:
        """Enhanced scan conversion with distance filtering"""
        ranges = np.array(scan_msg.ranges, dtype=float)
        angles = scan_msg.angle_min + np.arange(len(ranges)) * scan_msg.angle_increment
        
        # Filter valid points with distance constraints
        valid = (np.isfinite(ranges) & 
                (ranges >= self.MIN_OBSTACLE_DISTANCE) & 
                (ranges <= self.MAX_OBSTACLE_DISTANCE))
        
        if not np.any(valid):
            return []
            
        r = ranges[valid]
        a = angles[valid]
        xs = r * np.cos(a)
        ys = r * np.sin(a)
        
        return [(float(x), float(y)) for x, y in zip(xs, ys)]

    def transform_points(self, points_in_source_frame: List[Tuple[float, float]], 
                        transform_stamped) -> List[Tuple[float, float]]:
        """Batch transform points for better performance"""
        if not points_in_source_frame:
            return []

        transformed_points = []
        src_frame = getattr(transform_stamped, 'child_frame_id', '')
        stamp = transform_stamped.header.stamp

        for point in points_in_source_frame:
            p_stamped = PointStamped()
            p_stamped.header.frame_id = src_frame
            p_stamped.header.stamp = stamp
            p_stamped.point.x, p_stamped.point.y, p_stamped.point.z = point[0], point[1], 0.0
            
            try:
                p_transformed = tf2_geometry_msgs.do_transform_point(p_stamped, transform_stamped)
                transformed_points.append((p_transformed.point.x, p_transformed.point.y))
            except Exception as e:
                self.get_logger().debug(f"Point transform failed: {e}")

        return transformed_points

    def _predict_all_tracks(self, timestamp):
        """Predict all tracks to current timestamp"""
        with self._tracks_lock:
            for track in self.tracked_obstacles.values():
                dt = stamp_to_secs(timestamp) - stamp_to_secs(track.last_timestamp)
                if dt > 0:
                    track.predict(dt)

    def _publish_prediction_pointcloud(self, points: List[Tuple[float, float, float]], header: Header):
        """Publish prediction pointcloud"""
        if not points:
            return

        fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
        ]

        try:
            flat_data = [coord for point in points for coord in point]
            point_data = struct.pack(f'<{len(flat_data)}f', *flat_data)
            
            pc2 = PointCloud2(
                header=header,
                height=1,
                width=len(points),
                is_dense=False,
                is_bigendian=False,
                fields=fields,
                point_step=12,
                row_step=12 * len(points),
                data=point_data
            )
            self.obstacle_pub.publish(pc2)
        except Exception as e:
            self.get_logger().warning(f'Pointcloud publishing failed: {e}')

    def publish_clusters_as_pointcloud(self, clusters: List[List[Tuple[float, float]]], header: Header):
        """Publish clusters as pointcloud"""
        all_points = [p for cluster in clusters for p in cluster]
        if not all_points:
            return

        fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
        ]

        try:
            flat_data = [coord for point in all_points for coord in (*point, 0.0)]
            point_data = struct.pack(f'<{len(flat_data)}f', *flat_data)
            
            pc2 = PointCloud2(
                header=header,
                height=1,
                width=len(all_points),
                is_dense=True,
                is_bigendian=False,
                fields=fields,
                point_step=12,
                row_step=12 * len(all_points),
                data=point_data
            )
            self.cluster_pub.publish(pc2)
        except Exception as e:
            self.get_logger().debug(f'Cluster pointcloud failed: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()