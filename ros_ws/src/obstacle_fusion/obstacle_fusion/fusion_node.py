import rclpy
from rclpy.node import Node
from rclpy.time import Time
from collections import deque
from rclpy.duration import Duration
from dynamic_obstacle_detector_interfaces.msg import TrackedObject, TrackedObjectArray
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point, PointStamped, Vector3Stamped
import numpy as np
import threading
from scipy.optimize import linear_sum_assignment
from scipy import linalg
import tf2_ros
from tf2_ros import TransformException
from tf2_geometry_msgs import do_transform_point, do_transform_vector3
from tf2_msgs.msg import TFMessage
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

class GlobalTrackedObstacle:
    """
    A wrapper class to hold the state of an obstacle in the global view.
    It contains the latest fused estimation from all robots that have seen it.
    """
    def __init__(self, global_id, obstacle_state, header, robot_namespace):
        self.global_id = global_id
        self.robot_namespace = robot_namespace
        
        # Lifecycle management attributes
        self.status = 'tentative'  # Can be 'tentative' or 'confirmed'
        self.hits = 1              # Number of consecutive detections
        self.misses = 0            # Number of consecutive misses
        self.creation_time = Time.from_msg(header.stamp)

        self.update(obstacle_state, header)

    def update(self, obstacle_state, header):
        """Updates the state with the most recent observation or fused estimation."""
        self.state = obstacle_state
        self.last_seen_time = Time.from_msg(header.stamp)

    def confirm(self):
        """Promotes the track from 'tentative' to 'confirmed'."""
        if self.status == 'tentative':
            self.status = 'confirmed'
            # Optionally, log this event if a logger is available

    def register_hit(self, min_hits_to_confirm):
        """Registers a successful detection, potentially confirming the track."""
        self.misses = 0
        self.hits += 1
        if self.status == 'tentative' and self.hits >= min_hits_to_confirm:
            self.confirm()

    def register_miss(self):
        """Registers a missed detection."""
        self.hits = 0
        self.misses += 1

    def get_position(self):
        """Returns the obstacle's (x, y) position as a NumPy array for calculations."""
        return np.array([self.state.position.x, self.state.position.y])

    def predict(self, dt):
        """
        Predicts the next state of the obstacle using a constant velocity model.
        This increases the uncertainty (covariance) over time.
        This method now iterates in steps to prevent divergence with large dt.
        """
        remaining_dt = dt
        if remaining_dt <= 0:
            return

        # Loop prediction in smaller, stable steps if dt is large.
        while remaining_dt > 0:
            step_dt = min(remaining_dt, self.max_prediction_dt)
            remaining_dt -= step_dt

            # State transition matrix F for a constant velocity model
            F = np.array([
                [1, 0, step_dt, 0],
                [0, 1, 0, step_dt],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])

            # Process noise covariance matrix Q
            q_val = self.process_noise_variance * step_dt
            Q = np.array([
                [q_val, 0, 0, 0],
                [0, q_val, 0, 0],
                [0, 0, q_val, 0],
                [0, 0, 0, q_val]
            ])

            # Extract 4D state and 4x4 covariance
            indices_map = [0, 1, 3, 4]
            x_last = np.array([self.state.position.x, self.state.position.y, self.state.velocity.x, self.state.velocity.y])
            P_last = np.array(self.state.covariance).reshape(6, 6)[np.ix_(indices_map, indices_map)]

            # Apply velocity damping to simulate friction/drag over time.
            x_last[2] *= self.velocity_damping_factor
            x_last[3] *= self.velocity_damping_factor

            # Predict state: x_pred = F * x_last
            x_pred = F @ x_last
            # Predict covariance: P_pred = F * P_last * F.T + Q
            P_pred = F @ P_last @ F.T + Q

            # Update the state with the predicted values for the next iteration
            self.state.position.x, self.state.position.y = x_pred[0], x_pred[1]
            self.state.velocity.x, self.state.velocity.y = x_pred[2], x_pred[3]
            
            # Embed the predicted 4x4 covariance back into the 6x6 matrix
            P_pred_6x6 = np.array(self.state.covariance).reshape(6, 6)
            P_pred_6x6[np.ix_(indices_map, indices_map)] = P_pred
            self.state.covariance = P_pred_6x6.flatten().tolist()
    
class ObstacleFusionNode(Node):
    """
    ROS 2 Node responsible for fusing obstacle detections from multiple robots 
    into a single, consistent global view using data association and Kalman fusion.
    It also publishes an obstacle costmap for use with Nav2.
    """
    def __init__(self):
        super().__init__('obstacle_fusion_node')

        # --- PARAMETER DECLARATION ---
        # Define and retrieve all configurable parameters.
        self.declare_parameter('discovery_timer_period', 2.0) # Period to check for new robots
        self.declare_parameter('association_gate', 9.49) # Mahalanobis distance gate (chi-squared for 4-DOF at 95%).
        self.declare_parameter('track_lifetime', 2.0) # Time in seconds before a non-updated track is removed.
        self.declare_parameter('cleanup_period', 1.0) # Period to check for and remove stale tracks.
        self.declare_parameter('max_message_delay', 0.5) # Max age (s) of incoming messages to be considered valid
        self.declare_parameter('global_frame', 'map')
        self.declare_parameter('robot_filter_radius', 0.5) # Radius to filter out detections near known robot bases
        self.declare_parameter('spatial_pre_gate_distance', 2.0) # Max Euclidean distance for pre-gating before Mahalanobis
        self.declare_parameter('reprocessing_period', 0.1) # Period to re-process buffered messages
        self.declare_parameter('fusion_period', 0.1) # Period for the main fusion cycle (batch processing)
        self.declare_parameter('message_buffer_size', 50) # Max size of the message buffer for pending transforms.
        self.declare_parameter('buffer_overflow_policy', 'drop_oldest') # 'drop_oldest' or 'drop_newest'
        self.declare_parameter('transform_timeout_sec', 0.05) # Timeout for waiting on TF transforms
        self.declare_parameter('process_noise_variance', 0.1) # Variance for the KF process noise. Lowered for more stable predictions.
        self.declare_parameter('max_prediction_dt', 1.0) # Max time delta for a single prediction step to prevent divergence.
        self.declare_parameter('velocity_damping_factor', 0.98) # Damping factor for velocity on each prediction step (simulates friction).
        self.declare_parameter('min_hits_to_confirm', 3) # Hits needed to promote a track from 'tentative' to 'confirmed'.
        self.declare_parameter('max_age_for_confirmation', 2.0) # Max time (s) a track can be 'tentative'.
        self.declare_parameter('max_misses_to_delete', 5) # Consecutive misses before deleting a 'confirmed' track.
        self.declare_parameter('max_covariance_determinant', 10.0) # Max determinant of 2x2 pos covariance before deleting a track.

        self.DISCOVERY_PERIOD = self.get_parameter('discovery_timer_period').get_parameter_value().double_value
        self.ASSOCIATION_GATE = self.get_parameter('association_gate').get_parameter_value().double_value
        self.TRACK_LIFETIME = self.get_parameter('track_lifetime').get_parameter_value().double_value
        self.CLEANUP_PERIOD = self.get_parameter('cleanup_period').get_parameter_value().double_value
        self.MAX_MSG_DELAY = self.get_parameter('max_message_delay').get_parameter_value().double_value
        self.GLOBAL_FRAME = self.get_parameter('global_frame').get_parameter_value().string_value
        
        self.ROBOT_FILTER_RADIUS = self.get_parameter('robot_filter_radius').get_parameter_value().double_value
        self.SPATIAL_PRE_GATE_DISTANCE = self.get_parameter('spatial_pre_gate_distance').get_parameter_value().double_value
        self.REPROCESSING_PERIOD = self.get_parameter('reprocessing_period').get_parameter_value().double_value
        self.FUSION_PERIOD = self.get_parameter('fusion_period').get_parameter_value().double_value
        self.MESSAGE_BUFFER_SIZE = self.get_parameter('message_buffer_size').get_parameter_value().integer_value
        self.BUFFER_OVERFLOW_POLICY = self.get_parameter('buffer_overflow_policy').get_parameter_value().string_value
        self.TRANSFORM_TIMEOUT = self.get_parameter('transform_timeout_sec').get_parameter_value().double_value
        self.PROCESS_NOISE_VARIANCE = self.get_parameter('process_noise_variance').get_parameter_value().double_value
        self.MAX_PREDICTION_DT = self.get_parameter('max_prediction_dt').get_parameter_value().double_value
        self.VELOCITY_DAMPING_FACTOR = self.get_parameter('velocity_damping_factor').get_parameter_value().double_value
        self.MIN_HITS_TO_CONFIRM = self.get_parameter('min_hits_to_confirm').get_parameter_value().integer_value
        self.MAX_AGE_FOR_CONFIRMATION = self.get_parameter('max_age_for_confirmation').get_parameter_value().double_value
        self.MAX_MISSES_TO_DELETE = self.get_parameter('max_misses_to_delete').get_parameter_value().integer_value
        self.MAX_COVARIANCE_DETERMINANT = self.get_parameter('max_covariance_determinant').get_parameter_value().double_value

        # --- DATA STRUCTURES ---
        # Stores all currently tracked obstacles globally {global_id: GlobalTrackedObstacle}.
        self.global_obstacles = {} 
        self.next_global_id = 0
        # Set of known robot namespaces discovered through topic introspection.
        self.known_robots = set()
        # Dictionary of active subscribers for each robot's obstacle topic {topic_name: subscriber_object}.
        self.active_subscribers = {}
        # Buffer for messages waiting for a valid TF transform.
        self.message_buffer = deque(maxlen=self.MESSAGE_BUFFER_SIZE)
        # Buffer for transformed observations ready for batch fusion.
        self.observation_buffer = []
        # Thread lock to protect access to the observation_buffer.
        self.buffer_lock = threading.Lock()
        # Counter for messages dropped due to buffer overflow.
        self.dropped_messages_count = 0
        # Counter for pairs pruned by spatial pre-gating.
        self.pre_gated_pairs_count = 0
        # Thread lock to protect access to the global_obstacles dictionary.
        self.global_obstacles_lock = threading.Lock()

        # --- TF2 BUFFER AND LISTENER ---
        # TF buffer to store all received transforms.
        self.tf_buffer = tf2_ros.Buffer()
        # TF listener to populate the buffer from the /tf and /tf_static topics.
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        
        # --- PUBLISHERS ---
        # Publisher for the final, fused obstacle list.
        self.global_obstacles_pub = self.create_publisher(
            TrackedObjectArray,
            '/global_tracked_obstacles',
            10)
        
        # Publisher for RViz velocity vector markers.
        self.global_marker_pub = self.create_publisher(
            MarkerArray,
            '/global_velocity_markers',
            10)
        
        # Publisher for RViz covariance ellipse markers.
        self.global_covariance_pub = self.create_publisher(
            MarkerArray,
            '/global_covariance_markers',
            10)

        # --- DEBUG PUBLISHERS ---
        # Publisher per visualizzare le posizioni degli ostacoli trasformate prima della fusione
        self.debug_transformed_obstacles_pub = self.create_publisher(
            MarkerArray,
            '/debug/transformed_obstacles',
            10)
        # Enable or disable debug visualizations
        self.declare_parameter('enable_debug_visualizations', True)
        self.ENABLE_DEBUG_VIS = self.get_parameter('enable_debug_visualizations').get_parameter_value().bool_value


        # --- TIMERS ---
        # Periodically checks for new robot namespaces publishing obstacle data.
        self.discovery_timer = self.create_timer(self.DISCOVERY_PERIOD, self.discover_robots_callback)
        # Regularly removes stale obstacle tracks (those not seen recently).
        self.cleanup_timer = self.create_timer(self.CLEANUP_PERIOD, self.cleanup_tracks_callback)
        # Timer for the main batch fusion processing loop.
        self.fusion_timer = self.create_timer(self.FUSION_PERIOD, self._fusion_cycle_callback)
        # Timer to re-process messages that were waiting for a transform.
        self.reprocessing_timer = self.create_timer(self.REPROCESSING_PERIOD, self._reprocess_buffer_callback)

        self.get_logger().info("Obstacle fusion node started.")
        
    def discover_robots_callback(self):
        """
        Periodically scans for active topics to find new robots publishing
        on '/tracked_obstacles' and creates a new subscriber for each, 
        along with subscriptions to their namespaced TF topics.
        """
        topic_names_and_types = self.get_topic_names_and_types()
        target_topic_suffix = '/tracked_obstacles'
        target_msg_type = 'dynamic_obstacle_detector_interfaces/msg/TrackedObjectArray'

        for topic_name, msg_types in topic_names_and_types:
            if topic_name.endswith(target_topic_suffix) and target_msg_type in msg_types:
                # Extract the robot namespace from the topic name (e.g., /robot_name/tracked_obstacles).
                parts = topic_name.split('/')
                if len(parts) > 2 and parts[0] == '':
                    robot_namespace = parts[1]
                    self.known_robots.add(robot_namespace)
                    
                    # 1. Create Obstacle Subscriber
                    if topic_name not in self.active_subscribers:
                        self.get_logger().info(f"Discovered new robot: '{robot_namespace}' on topic: {topic_name}")

                        # Use Best Effort QoS for high-frequency sensor data.
                        qos_profile = QoSProfile(
                            reliability=ReliabilityPolicy.BEST_EFFORT,
                            history=HistoryPolicy.KEEP_LAST,
                            depth=1
                        )

                        # Create a subscription with a lambda to pass the robot_namespace to the callback.
                        new_sub = self.create_subscription(
                            TrackedObjectArray,
                            topic_name,
                            lambda msg, ns=robot_namespace: self.robot_obstacles_callback(msg, ns),
                            qos_profile
                        )
                        self.active_subscribers[topic_name] = new_sub

    def _normalize_covariance(self, covariance_list, robot_namespace=""):
        """
        Ensures a covariance is a 6x6 matrix (36 elements).
        - If 4x4 (16 elements), expands it to 6x6.
        - If other size, creates a new 6x6 diagonal matrix with high uncertainty.
        """
        if len(covariance_list) == 36:
            return covariance_list

        self.get_logger().debug(f"Normalizing covariance from '{robot_namespace}' (length: {len(covariance_list)}) to 6x6.")
        
        # Default: high but realistic uncertainty for unobserved states.
        # [x, y, z, vx, vy, vz]
        default_variances = np.array([10.0, 10.0, 10.0, 100.0, 100.0, 100.0])
        cov_6x6 = np.diag(default_variances)

        if len(covariance_list) == 16:
            # Expand from 4x4 [x, y, vx, vy] to 6x6
            cov_4x4 = np.array(covariance_list).reshape(4, 4)
            indices_map_4d = [0, 1, 3, 4]  # x, y, vx, vy
            cov_6x6.fill(0) # Reset to zero before filling
            cov_6x6[np.ix_(indices_map_4d, indices_map_4d)] = cov_4x4
            # Assign realistic uncertainty to unobserved dimensions
            cov_6x6[2, 2] = 10.0  # z variance
            cov_6x6[5, 5] = 100.0 # vz variance
        
        # Ensure diagonal has at least a small value for stability
        np.fill_diagonal(cov_6x6, np.maximum(np.diag(cov_6x6), 1e-9))
        return cov_6x6.flatten().tolist()

    def _reprocess_buffer_callback(self):
        """Periodically tries to process messages stored in the buffer."""
        processed_count = 0
        # Iterate over a copy, as we might modify the deque
        for _ in range(len(self.message_buffer)):
            msg, robot_namespace = self.message_buffer.popleft()
            
            # Check if the message has expired while in the buffer
            now = self.get_clock().now()
            msg_time = Time.from_msg(msg.header.stamp)
            delay = (now - msg_time).nanoseconds / 1e9
            if delay > self.MAX_MSG_DELAY:
                self.get_logger().debug(f"Dropping expired message from buffer (from '{robot_namespace}').")
                continue

            # Try to transform and process again
            if self._transform_and_process_obstacles(msg, robot_namespace):
                processed_count += 1
            else:
                # If it still fails, put it back at the end of the queue
                self.message_buffer.append((msg, robot_namespace))
        
        if processed_count > 0:
            self.get_logger().debug(f"Successfully processed {processed_count} messages from the buffer.")

    def robot_obstacles_callback(self, msg, robot_namespace):
        """
        Callback for obstacle messages. It validates the message time and
        attempts to process it immediately. If transformation fails, it buffers the message.
        """
        now = self.get_clock().now()
        msg_time = Time.from_msg(msg.header.stamp)
        delay = (now - msg_time).nanoseconds / 1e9
        
        # Discard messages that are too old to be relevant.
        if delay > self.MAX_MSG_DELAY:
            self.get_logger().warn(
                f"Discarding old message from '{robot_namespace}' (delay: {delay:.3f}s > {self.MAX_MSG_DELAY}s)"
            )
            return

        # Attempt to process the message immediately.
        if not self._transform_and_process_obstacles(msg, robot_namespace):
            # If transformation fails, buffer the message for reprocessing, handling potential overflow.
            if len(self.message_buffer) >= self.message_buffer.maxlen:
                self.dropped_messages_count += 1
                if self.BUFFER_OVERFLOW_POLICY == 'drop_newest':
                    self.get_logger().warn(
                        f"Message buffer full. Dropping newest message from '{robot_namespace}'. "
                        f"Total dropped: {self.dropped_messages_count}."
                    )
                    return # Do not add the new message
                else: # 'drop_oldest' is the default
                    self.get_logger().warn(
                        f"Message buffer full. Dropping oldest message to make space for new one from '{robot_namespace}'. "
                        f"Total dropped: {self.dropped_messages_count}."
                    )
            self.message_buffer.append((msg, robot_namespace)) # deque handles dropping the oldest if maxlen is reached
            self.get_logger().debug(f"Buffered message from '{robot_namespace}'. Buffer size: {len(self.message_buffer)}/{self.message_buffer.maxlen}")

    def _transform_and_process_obstacles(self, msg, robot_namespace):
        """
        Performs TF transformation and adds processed obstacles to the observation buffer.
        Returns True on success, False on transformation failure.
        """
        transformed_objects = []
        transform = None

        if msg.header.frame_id == self.GLOBAL_FRAME:
            # No transformation needed, use objects directly
            transformed_objects = [obs for obs in msg.objects]
        else:
            # Transformation is needed
            target_frame = self.GLOBAL_FRAME
            source_frame = msg.header.frame_id
            
            # Check if transform is available at the message timestamp
            try:
                # Retrieve the transform from source to target frame at the message timestamp.
                # The timeout waits briefly that the transformation becomes available.
                if not self.tf_buffer.can_transform(target_frame, source_frame, msg.header.stamp, timeout=Duration(seconds=self.TRANSFORM_TIMEOUT)):
                    self.get_logger().debug(f"Transform from '{source_frame}' to '{target_frame}' not available at timestamp {msg.header.stamp.sec}.{msg.header.stamp.nanosec}. Buffering message.")
                    return False # Failed, The message will be buffered
                
                transform = self.tf_buffer.lookup_transform(target_frame, source_frame, msg.header.stamp)
            except TransformException as ex:
                self.get_logger().warn(f"Failed to look up transform from '{source_frame}' to '{target_frame}': {ex}. Buffering message.")
                return False # Failed, The message will be buffered

            try:
                for obs in msg.objects:
                    # Transform the position and velocity.
                    pos_stamped = PointStamped(header=msg.header, point=obs.position)
                    transformed_pos_stamped = do_transform_point(pos_stamped, transform)
                    transformed_pos = transformed_pos_stamped.point

                    # --- CORRECT VELOCITY TRANSFORMATION ---
                    # do_transform_vector3 only applies rotation, which is incorrect for velocities
                    # between moving frames. We must manually apply the rotation part of the transform.
                    from scipy.spatial.transform import Rotation as R

                    # 1. Get the rotation from the transform
                    q = transform.transform.rotation
                    rotation = R.from_quat([q.x, q.y, q.z, q.w])

                    # 2. Convert the original velocity vector to a numpy array
                    original_vel = np.array([obs.velocity.x, obs.velocity.y, obs.velocity.z])

                    # 3. Rotate the velocity vector
                    rotated_vel = rotation.apply(original_vel)

                    # The velocity in the target frame is the rotated velocity.
                    # Note: This assumes the fusion node's Kalman filter will handle the frame's velocity component.
                    # The prediction step in the global frame implicitly handles this.
                    # Create a new TrackedObject with transformed data.
                    new_obs = TrackedObject()
                    new_obs.id = obs.id
                    new_obs.position.x, new_obs.position.y, new_obs.position.z = transformed_pos.x, transformed_pos.y, 0.0
                    new_obs.velocity.x, new_obs.velocity.y, new_obs.velocity.z = rotated_vel[0], rotated_vel[1], rotated_vel[2]
                    new_obs.covariance = self._normalize_covariance(obs.covariance, robot_namespace)
                    transformed_objects.append(new_obs)
            except TransformException as ex:
                self.get_logger().warn(f"Error during point/vector transformation: {ex}")
                return False

        # The rest of the processing logic is now part of this method.
        with self.buffer_lock:
            self.observation_buffer.append((transformed_objects, msg.header, robot_namespace))
        
        if self.ENABLE_DEBUG_VIS:
            self._publish_debug_markers(transformed_objects, msg.header, robot_namespace)
        return True  # Indicate success

    def _fusion_cycle_callback(self):
        """Main processing loop that runs periodically to fuse all buffered observations."""
        if not self.observation_buffer:
            return

        # Take all observations from the buffer for this cycle.
        with self.buffer_lock:
            current_observations_batch = self.observation_buffer
            self.observation_buffer = []
            
        # 1. PRE-PROCESS: Flatten and filter all observations from the batch.
        all_filtered_observations = []
        robot_positions = {}
        for ns in self.known_robots:
            # Get the position of the known robot's base in the global frame.
            try:
                transform = self.tf_buffer.lookup_transform(
                    self.GLOBAL_FRAME, f"{ns}/base_footprint", Time()
                )
                robot_positions[ns] = np.array([
                    transform.transform.translation.x,
                    transform.transform.translation.y
                ])
            except TransformException:
                # Log a debug warning if a robot's transform isn't available.
                self.get_logger().debug(f"Could not get position for robot '{ns}'.")

        for transformed_objects, header, robot_namespace in current_observations_batch:
            for obs in transformed_objects:
                obs_pos = np.array([obs.position.x, obs.position.y])
                is_another_robot = False
                for robot_pos in robot_positions.values():
                    # If the obstacle is within the exclusion radius of a known robot, filter it out.
                    if np.linalg.norm(obs_pos - robot_pos) < self.ROBOT_FILTER_RADIUS:
                        is_another_robot = True
                        break
                if not is_another_robot:
                    # Store the observation along with its original header and source.
                    all_filtered_observations.append({'obs': obs, 'header': header, 'ns': robot_namespace})

        if not all_filtered_observations:
            return

        # 2. ASSOCIATE all filtered observations with existing global tracks.
        with self.global_obstacles_lock:
            if not self.global_obstacles:
                # If no global tracks, create new ones for all filtered objects.
                for item in all_filtered_observations:
                    self.create_new_global_obstacle(item['obs'], item['header'], item['ns'])
            else:

                # --- IMMEDIATE COVARIANCE CLEANUP ---
                # Immediately remove tracks whose covariance has grown too large after prediction,
                # before they can participate in association.
                tracks_to_remove_immediately = []
                for gid, track in self.global_obstacles.items():
                    try:
                        cov_full = np.array(track.state.covariance).reshape(6, 6)
                        cov_xy = cov_full[0:2, 0:2]
                        determinant = np.linalg.det(cov_xy)
                        if determinant > self.MAX_COVARIANCE_DETERMINANT:
                            tracks_to_remove_immediately.append(gid)
                            self.get_logger().debug(f"Immediately removing track {gid} post-prediction due to excessive covariance (det: {determinant:.2f}).")
                    except (np.linalg.LinAlgError, IndexError):
                        continue # Skip if covariance is malformed

                if tracks_to_remove_immediately:
                    delete_marker_array = MarkerArray()
                    for gid in tracks_to_remove_immediately:
                        if gid in self.global_obstacles:
                            del self.global_obstacles[gid]
                            delete_marker_array.markers.append(Marker(action=Marker.DELETE, ns="global_velocity_vectors", id=gid))
                    self.global_marker_pub.publish(delete_marker_array)

                # --- ASSOCIATION STEP (as before) ---
                # Use the Hungarian algorithm for optimal assignment (Munkres).
                LARGE_COST = 1e9
                global_ids = list(self.global_obstacles.keys())
                n_globals = len(global_ids)
                n_received = len(all_filtered_observations)
                
                # Initialize a cost matrix with a high value for non-associated pairs.
                cost_matrix = np.full((n_globals, n_received), LARGE_COST, dtype=float)
                self.pre_gated_pairs_count = 0

                # Calculate the cost (Mahalanobis distance) for every global track/observation pair.
                for i, gid in enumerate(global_ids):
                    global_track = self.global_obstacles[gid]

                    for j, item in enumerate(all_filtered_observations):
                        # --- DYNAMIC PREDICTION STEP ---
                        # Predict the track's state to the specific timestamp of the current observation.
                        # This is the key change to fix duplicate tracks.
                        observation_time = Time.from_msg(item['header'].stamp)
                        dt = (observation_time - global_track.last_seen_time).nanoseconds / 1e9
                        
                        # Create a temporary predicted state for this association check
                        # We cannot modify the original track yet.
                        predicted_track = GlobalTrackedObstacle(
                            global_track.global_id, global_track.state, item['header'], global_track.robot_namespace
                        )
                        predicted_track.state.covariance = list(global_track.state.covariance) # Deep copy
                        predicted_track.max_prediction_dt = self.MAX_PREDICTION_DT
                        predicted_track.velocity_damping_factor = self.VELOCITY_DAMPING_FACTOR
                        predicted_track.process_noise_variance = self.PROCESS_NOISE_VARIANCE
                        predicted_track.predict(dt)

                        # Extract 4D state and covariance from the *predicted* track
                        track_pos = predicted_track.get_position()
                        global_state = np.array([predicted_track.state.position.x, predicted_track.state.position.y, predicted_track.state.velocity.x, predicted_track.state.velocity.y])
                        P_global_full = np.array(predicted_track.state.covariance).reshape(6, 6)
                        P_global = P_global_full[np.ix_([0, 1, 3, 4], [0, 1, 3, 4])]


                        new_obs = item['obs']
                        obs_pos = np.array([new_obs.position.x, new_obs.position.y])

                        # --- SPATIAL PRE-GATING ---
                        # Quickly discard pairs that are too far apart before expensive calculations.
                        euclidean_dist = np.linalg.norm(track_pos - obs_pos)
                        if euclidean_dist > self.SPATIAL_PRE_GATE_DISTANCE:
                            self.pre_gated_pairs_count += 1
                            continue # Skip to the next observation


                        # Extract 4D observation vector [x, y, vx, vy].
                        obs_state = np.array([
                            new_obs.position.x, new_obs.position.y,
                            new_obs.velocity.x, new_obs.velocity.y
                        ])
                        # Normalize and extract 4x4 observation covariance matrix R.
                        R_obs_full = np.array(new_obs.covariance).reshape(6, 6)
                        R_obs = R_obs_full[np.ix_([0, 1, 3, 4], [0, 1, 3, 4])]

                        # Calculate the Mahalanobis distance squared (cost metric).
                        y = obs_state - global_state      # Innovation (residual)
                        S = P_global + R_obs              # Innovation covariance
                        
                        # Add a small value to the diagonal for numerical stability.
                        S += np.eye(S.shape[0]) * 1e-6

                        try:
                            # Use pseudo-inverse for stability in the Mahalanobis calculation.
                            mahal_sq = y.T @ np.linalg.pinv(S) @ y
                            if mahal_sq < self.ASSOCIATION_GATE:
                                # Only use cost if it's within the gating threshold.
                                cost_matrix[i, j] = mahal_sq
                        except np.linalg.LinAlgError:
                            # If the matrix is singular, skip the pair.
                            continue
                
                if self.pre_gated_pairs_count > 0:
                    self.get_logger().debug(f"Association: Pruned {self.pre_gated_pairs_count} pairs with spatial pre-gating.")


                # Run the Hungarian algorithm for optimal assignment.
                assigned_track_indices, assigned_obs_indices = linear_sum_assignment(cost_matrix)

                # 3. FUSE matched tracks and create new ones for unmatched objects.
                # Explicitly separate valid matches from high-cost "forced" assignments.
                matched_pairs = []
                # Initially, assume all are unmatched.
                unmatched_track_indices = set(range(n_globals))
                unmatched_observation_indices = set(range(n_received))

                for track_idx, obs_idx in zip(assigned_track_indices, assigned_obs_indices):
                    # A valid match must have a cost below the gate.
                    if cost_matrix[track_idx, obs_idx] < self.ASSOCIATION_GATE:
                        matched_pairs.append((track_idx, obs_idx))
                        unmatched_track_indices.discard(track_idx)
                        unmatched_observation_indices.discard(obs_idx)
                
                self.get_logger().debug(f"Association results: {len(matched_pairs)} matched, {len(unmatched_track_indices)} unmatched tracks, {len(unmatched_observation_indices)} new observations.")

                # --- FUSION STEP for matched pairs ---
                for track_idx, obs_idx in matched_pairs:
                        gid = global_ids[track_idx]
                        global_track = self.global_obstacles[gid]
                        item = all_filtered_observations[obs_idx]
                        new_observation, header, robot_namespace = item['obs'], item['header'], item['ns']

                        # --- Information Filter / Kalman Fusion Update ---
                        # Before fusing, we must ensure the global track is predicted to the observation's time.
                        # This was done for association, now we do it for the actual update.
                        observation_time = Time.from_msg(header.stamp)
                        dt = (observation_time - global_track.last_seen_time).nanoseconds / 1e9
                        if dt > 0:
                            global_track.predict(dt)

                        try:
                            # Extract 4x4 covariance and 4D state vectors [x, y, vx, vy].
                            indices_map = [0, 1, 3, 4]
                            P_global_full = np.array(global_track.state.covariance).reshape(6, 6)
                            R_obs_full = np.array(new_observation.covariance).reshape(6, 6)
                            P = P_global_full[np.ix_(indices_map, indices_map)] # Current estimate covariance (predicted)
                            R = R_obs_full[np.ix_(indices_map, indices_map)]    # Measurement covariance

                            x_global = np.array([global_track.state.position.x, global_track.state.position.y, global_track.state.velocity.x, global_track.state.velocity.y])
                            z_obs = np.array([new_observation.position.x, new_observation.position.y, new_observation.velocity.x, new_observation.velocity.y])

                            # 1. Calculate Kalman Gain (K = P * inv(P + R))
                            S = P + R  # Innovation covariance
                            try:
                                # Use Cholesky decomposition for a fast and stable solve.
                                # This is the preferred method for SPD matrices.
                                L = linalg.cholesky(S, lower=True)
                                K_T = linalg.cho_solve((L, True), P.T)
                                K = K_T.T
                            except linalg.LinAlgError:
                                # Fallback to pseudo-inverse if S is not positive-definite.
                                self.get_logger().warn(f"Cholesky decomposition failed for track {gid}. Falling back to pseudo-inverse.")
                                S_jittered = S + np.eye(S.shape[0]) * 1e-6
                                K = P @ np.linalg.pinv(S_jittered)

                            # 2. Update state (x_fused = x_global + K * (z_obs - x_global))
                            y = z_obs - x_global # Innovation
                            x_fused = x_global + K @ y

                            # 3. Update covariance (P_fused = (I - K) * P)
                            I = np.eye(K.shape[0])
                            P_fused = (I - K) @ P

                            # Reconstruct the 6D state and covariance for publishing.
                            fused_state = TrackedObject()
                            fused_state.id = gid
                            fused_state.position.x, fused_state.position.y = x_fused[0], x_fused[1]
                            fused_state.velocity.x, fused_state.velocity.y = x_fused[2], x_fused[3]

                            # Embed the 4x4 fused covariance back into a 6x6 matrix.
                            P_fused_6x6 = np.zeros((6, 6))
                            P_fused_6x6[np.ix_(indices_map, indices_map)] = P_fused
                            fused_state.covariance = P_fused_6x6.flatten().tolist()

                        except (np.linalg.LinAlgError, ValueError) as e:
                            self.get_logger().warn(f"Kalman fusion failed for track {gid}: {e}. Using latest observation as fallback.")
                            # Fallback: use the latest observation but maintain the global ID and structure.
                            fused_state = TrackedObject()
                            fused_state.id = gid
                            fused_state.position = new_observation.position
                            fused_state.velocity = new_observation.velocity
                            # The covariance is already normalized to 6x6 at this point.
                            fused_state.covariance = new_observation.covariance

                        # Update the global track with the fused state.
                        global_track.update(fused_state, header)
                        # Register the successful match for lifecycle management.
                        global_track.register_hit(self.MIN_HITS_TO_CONFIRM)

                # --- LIFECYCLE STEP: Mark unmatched tracks as missed ---
                for track_idx in unmatched_track_indices:
                    gid = global_ids[track_idx]
                    self.global_obstacles[gid].register_miss()

                # --- LIFECYCLE STEP: Create new tracks for unmatched observations ---
                for obs_idx in unmatched_observation_indices:
                    item = all_filtered_observations[obs_idx]
                    self.create_new_global_obstacle(item['obs'], item['header'], item['ns'])

        # Publish the updated list after the fusion cycle is complete.
        self.publish_global_obstacles()
            
    def create_new_global_obstacle(self, obstacle_msg, header, robot_namespace):
        """Initializes and registers a new global obstacle track with a unique ID."""
        # This method is called within _fusion_cycle_callback, which already holds the lock.
        new_id = self.next_global_id
        
        # Pass prediction parameters to the new track instance
        global_obstacle = GlobalTrackedObstacle(new_id, obstacle_msg, header, robot_namespace)        
        # Inject node parameters into the track instance for its methods to use.
        global_obstacle.max_prediction_dt = self.MAX_PREDICTION_DT
        global_obstacle.velocity_damping_factor = self.VELOCITY_DAMPING_FACTOR
        global_obstacle.process_noise_variance = self.PROCESS_NOISE_VARIANCE

        self.global_obstacles[new_id] = global_obstacle
        self.next_global_id += 1
        self.get_logger().debug(f"Created new global obstacle ID: {new_id} from '{robot_namespace}'")

    def cleanup_tracks_callback(self):
        """
        Removes global obstacle tracks that have not been updated for longer than 
        the defined track lifetime.
        """
        now = self.get_clock().now()
        tracks_to_remove = []
        
        with self.global_obstacles_lock:
            for gid, track in self.global_obstacles.items():
                age = (now - track.creation_time).nanoseconds / 1e9
                
                # Deletion policy for tentative tracks
                if track.status == 'tentative':
                    # Remove if it's too old and hasn't been confirmed
                    if age > self.MAX_AGE_FOR_CONFIRMATION:
                        tracks_to_remove.append(gid)
                        self.get_logger().debug(f"Removing tentative track {gid} (unconfirmed timeout).")
                        continue
                
                # Deletion policy for all tracks based on misses
                if track.misses > self.MAX_MISSES_TO_DELETE:
                    tracks_to_remove.append(gid)
                    self.get_logger().debug(f"Removing track {gid} (missed {track.misses} times).")

            # --- New check for covariance size ---
            for gid, track in self.global_obstacles.items():
                if gid in tracks_to_remove: continue # Already marked for deletion
                try:
                    # Extract 2x2 positional covariance [x, y]
                    cov_full = np.array(track.state.covariance).reshape(6, 6)
                    cov_xy = cov_full[0:2, 0:2]
                    
                    # The determinant is a scalar measure of the uncertainty area
                    determinant = np.linalg.det(cov_xy)
                    
                    if determinant > self.MAX_COVARIANCE_DETERMINANT:
                        tracks_to_remove.append(gid)
                        self.get_logger().debug(f"Removing track {gid} due to excessive covariance (det: {determinant:.2f} > {self.MAX_COVARIANCE_DETERMINANT}).")
                except (np.linalg.LinAlgError, IndexError) as e:
                    self.get_logger().warn(f"Could not check covariance for track {gid}: {e}")
            if tracks_to_remove:
                delete_marker_array = MarkerArray()
                for gid in tracks_to_remove:
                    # Ensure we don't try to delete a key that's already gone
                    if gid not in self.global_obstacles: continue
                    delete_marker = Marker(action=Marker.DELETE, ns="global_velocity_vectors", id=gid)
                    delete_marker_array.markers.append(delete_marker)
                    del self.global_obstacles[gid]
                    self.get_logger().debug(f"Removed global obstacle ID {gid} due to timeout.")
                self.global_marker_pub.publish(delete_marker_array)
        
        # Log di debug per i track rimossi
        if tracks_to_remove:
            self.get_logger().debug(f"Removed {len(tracks_to_remove)} stale tracks.")

    def publish_global_obstacles(self):
        """Builds and publishes the global TrackedObjectArray and visualization markers."""
        global_array_msg = TrackedObjectArray()
        global_array_msg.header.stamp = self.get_clock().now().to_msg()
        global_array_msg.header.frame_id = self.GLOBAL_FRAME

        marker_array = MarkerArray()
        covariance_marker_array = MarkerArray()
                
        with self.global_obstacles_lock:
            for gid, global_track in self.global_obstacles.items():
                # Populate the TrackedObject message from the GlobalTrackedObstacle state.
                pub_obj_msg = TrackedObject()
                pub_obj_msg.id = gid
                pub_obj_msg.position = global_track.state.position
                pub_obj_msg.velocity = global_track.state.velocity
                pub_obj_msg.covariance = global_track.state.covariance
                global_array_msg.objects.append(pub_obj_msg)

                # Create an Arrow marker to visualize the obstacle's velocity.
                pos = pub_obj_msg.position
                vel = pub_obj_msg.velocity
                marker = Marker()
                marker.header = global_array_msg.header
                marker.ns = "global_velocity_vectors"
                marker.id = gid
                marker.type = Marker.ARROW
                marker.action = Marker.ADD
                # Arrow points from current position to a point scaled by velocity.
                marker.points = [pos, Point(x=pos.x + vel.x, y=pos.y + vel.y, z=0.0)]
                marker.scale.x = 0.05
                marker.scale.y = 0.1
                # Set marker lifetime slightly longer than track lifetime to prevent immediate disappearance.
                marker.lifetime = Duration(seconds=self.TRACK_LIFETIME * 1.5).to_msg() 

                # Color-code markers based on track status
                if global_track.status == 'confirmed':
                    marker.color.a = 0.9  # Solid
                    marker.color.r = 1.0  # Orange
                    marker.color.g = 0.5
                    marker.color.b = 0.0
                else: # 'tentative'
                    marker.color.a = 0.5  # Semi-transparent
                    marker.color.r = 1.0  # Yellow
                    marker.color.g = 1.0
                    marker.color.b = 0.0
                marker_array.markers.append(marker)

                # --- Create Covariance Ellipse Marker ---
                # Only for confirmed tracks to reduce visual clutter.
                if global_track.status == 'confirmed':
                    try:
                        # Extract 2x2 positional covariance [x, y]
                        cov_full = np.array(pub_obj_msg.covariance).reshape(6, 6)
                        cov_xy = cov_full[0:2, 0:2]

                        # Calculate eigenvalues and eigenvectors for the 2D ellipse
                        eigenvalues, eigenvectors = np.linalg.eigh(cov_xy)
                        
                        # The angle of the major axis is the angle of the first eigenvector
                        angle = np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0])
                        
                        # Quaternion from yaw angle
                        q_w = np.cos(angle / 2.0)
                        q_z = np.sin(angle / 2.0)

                        # Scale axes based on eigenvalues for a 95% confidence interval
                        chi2_val = 5.991  # Chi-squared value for 2-DOF, 95%
                        scale_x = 2 * np.sqrt(eigenvalues[0] * chi2_val)
                        scale_y = 2 * np.sqrt(eigenvalues[1] * chi2_val)

                        cov_marker = Marker()
                        cov_marker.header = global_array_msg.header
                        cov_marker.ns = "global_covariance_ellipses"
                        cov_marker.id = gid
                        cov_marker.type = Marker.SPHERE
                        cov_marker.action = Marker.ADD
                        cov_marker.pose.position = pos
                        cov_marker.pose.orientation.w = q_w
                        cov_marker.pose.orientation.z = q_z
                        cov_marker.scale.x = max(scale_x, 0.01) # Ensure a minimum size
                        cov_marker.scale.y = max(scale_y, 0.01)
                        cov_marker.scale.z = 0.01 # Flat ellipse
                        cov_marker.color.a = 0.3 # Semi-transparent
                        cov_marker.color.r = 1.0
                        cov_marker.color.g = 0.5
                        cov_marker.color.b = 0.0
                        cov_marker.lifetime = Duration(seconds=self.TRACK_LIFETIME * 1.5).to_msg()
                        covariance_marker_array.markers.append(cov_marker)
                    except (np.linalg.LinAlgError, IndexError) as e:
                        self.get_logger().warn(f"Could not compute covariance ellipse for track {gid}: {e}")
            
        self.global_obstacles_pub.publish(global_array_msg)
        if marker_array.markers:
            self.global_marker_pub.publish(marker_array)
        if covariance_marker_array.markers:
            self.global_covariance_pub.publish(covariance_marker_array)

    def _publish_debug_markers(self, transformed_objects, header, robot_namespace):
        """Pubblica MarkerArray per visualizzare le posizioni trasformate per il debug."""
        if not self.ENABLE_DEBUG_VIS:
            return

        marker_array = MarkerArray()
        marker_id = 0
        for obs in transformed_objects:
            marker = Marker()
            marker.header.frame_id = self.GLOBAL_FRAME
            marker.header.stamp = header.stamp
            marker.ns = f"transformed_{robot_namespace}"
            marker.id = marker_id
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.pose.position = obs.position
            marker.pose.orientation.w = 1.0
            marker.scale.x = 0.15
            marker.scale.y = 0.15
            marker.scale.z = 0.15
            marker.color.a = 0.8
            # Paint each robot's obstacles a different color based on a hash of its namespace.
            hash_val = hash(robot_namespace)
            marker.color.r = (hash_val & 0xFF) / 255.0
            marker.color.g = ((hash_val >> 8) & 0xFF) / 255.0
            marker.color.b = ((hash_val >> 16) & 0xFF) / 255.0
            marker.lifetime = Duration(seconds=2.0).to_msg()
            marker_array.markers.append(marker)
            marker_id += 1
        self.debug_transformed_obstacles_pub.publish(marker_array)

def main(args=None):
    """
    Main entry point for the ROS 2 node. Initializes and spins the ObstacleFusionNode.
    """
    rclpy.init(args=args)
    fusion_node = ObstacleFusionNode()
    rclpy.spin(fusion_node)
    fusion_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()