import os
import yaml
import tempfile

def create_namespaced_bridge_yaml(base_yaml_path, namespace):
    """
    Generate a temporary, namespaced bridge YAML file for the ros_gz_bridge.

    This function reads a base bridge configuration, prepends a namespace to each
    ROS and Gazebo topic, and saves the result to a temporary file. This is
    essential for multi-robot simulations to ensure that each robot's topics
    are isolated (e.g., '/tb1/cmd_vel', '/tb2/cmd_vel'). Global topics like
    '/clock' and '/tf' are intentionally excluded from namespacing.

    Args:
        base_yaml_path (str): The file path to the base bridge YAML configuration.
        namespace (str): The robot-specific namespace to apply (e.g., 'tb1').

    Returns:
        str: The file path to the newly created temporary namespaced YAML file.
    """
    with open(base_yaml_path, 'r') as f:
        bridges = yaml.safe_load(f)

    if namespace and not namespace.endswith('/'):
        namespace_with_slash = namespace + '/'
    else:
        namespace_with_slash = namespace

    namespaced_bridges = []
    for bridge in bridges:
        # On the ROS side, namespace all topics except for global ones like 'clock' and 'tf'.
        # The '/tf' topic is later remapped to a global scope in the launch file for Nav2.
        if bridge['ros_topic_name'] not in ['clock', 'tf']:
            bridge['ros_topic_name'] = f"{namespace_with_slash}{bridge['ros_topic_name']}"

        # On the Gazebo side, namespace all topics except for the global 'clock'.
        # This ensures the bridge subscribes to the correct namespaced Gazebo topics (e.g., '/tb1/odom').
        if bridge['gz_topic_name'] not in ['clock']:
            bridge['gz_topic_name'] = f"{namespace_with_slash}{bridge['gz_topic_name']}"
            
        namespaced_bridges.append(bridge)

    output_path = os.path.join(tempfile.gettempdir(), f"{namespace.strip('/')}_bridge.yaml")
    with open(output_path, 'w') as f:
        yaml.dump(namespaced_bridges, f)

    return output_path

def load_sdf_with_namespace(model_path, namespace):
    """
    Patch an SDF file with a robot namespace to isolate topics and frames.

    This function performs a text-based replacement on an SDF file to prepend a
    namespace to all relevant tags, such as topics and frame IDs. This is a
    necessary workaround because some Gazebo plugins do not automatically
    namespace their topics based on the model name, leading to conflicts in a
    multi-robot simulation. The current replacements are specific to TurtleBot3.

    Args:
        model_path (str): The file path to the original SDF model.
        namespace (str): The robot-specific namespace to apply (e.g., 'tb1').

    Returns:
        str: The patched SDF content as a string.
    """
    with open(model_path, 'r') as f:
        sdf_text = f.read()

    topic_map = {
        '<tf_topic>/tf</tf_topic>': f'<tf_topic>/{namespace}/tf</tf_topic>',
        '<topic>imu</topic>': f'<topic>{namespace}/imu</topic>',
        '<topic>scan</topic>': f'<topic>{namespace}/scan</topic>',
        '<topic>cmd_vel</topic>': f'<topic>{namespace}/cmd_vel</topic>',
        '<odom_topic>odom</odom_topic>': f'<odom_topic>{namespace}/odom</odom_topic>',
        '<frame_id>odom</frame_id>': f'<frame_id>{namespace}/odom</frame_id>',
        '<child_frame_id>base_footprint</child_frame_id>': f'<child_frame_id>{namespace}/base_footprint</child_frame_id>',
        '<frame_id>base_link</frame_id>': f'<frame_id>{namespace}/base_link</frame_id>',
        '<frame_id>base_scan</frame_id>': f'<frame_id>{namespace}/base_scan</frame_id>',
        '<gz_frame_id>base_scan</gz_frame_id>': f'<gz_frame_id>{namespace}/base_scan</gz_frame_id>',
        '<frame_id>imu_link</frame_id>': f'<frame_id>{namespace}/imu_link</frame_id>',
        '<topic>joint_states</topic>': f'<topic>{namespace}/joint_states</topic>',
        '<topic>camera/image_raw</topic>': f'<topic>{namespace}/camera/image_raw</topic>',
        '<camera_info_topic>camera/camera_info</camera_info_topic>': f'<camera_info_topic>{namespace}/camera/camera_info</camera_info_topic>',
    }

    for original, replacement in topic_map.items():
        sdf_text = sdf_text.replace(original, replacement)

    return sdf_text

def generate_rviz_config(robot_name, base_config_path):
    """
    Generate a robot-specific RViz configuration file from a template.

    This function takes a base RViz configuration file and replaces a placeholder
    string ('<ROBOT_NAME>') with the actual robot's name. This allows each robot
    to have its own RViz instance configured to display its specific topics and
    TF frames. The new configuration is saved to a temporary file.

    Args:
        robot_name (str): The name of the robot (e.g., 'tb1').
        base_config_path (str): The file path to the template RViz configuration.

    Returns:
        str: The file path to the newly created temporary RViz configuration.
    """
    with open(base_config_path, 'r') as f:
        config = f.read()

    config = config.replace('<ROBOT_NAME>', robot_name)

    temp_dir = tempfile.gettempdir()
    output_config_path = os.path.join(temp_dir, f'{robot_name}_rviz_config.rviz')

    with open(output_config_path, 'w') as f:
        f.write(config)

    return output_config_path

def generate_namespaced_nav2_params(base_params_path, namespace):
    """
    Generate namespaced Nav2 parameters for multi-robot setup.
    """
    with open(base_params_path, 'r') as f:
        params = yaml.safe_load(f)

    namespaced_params = {}
    for key, value in params.items():
        node_key = f"{namespace}/{key}"
        namespaced_params[node_key] = value

    def apply_namespace(data, ns):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    if key in ['robot_base_frame', 'base_frame_id', 'base_frame']:
                        if value == 'base_footprint' and not value.startswith(f"{ns}/"):
                            data[key] = f"{ns}/{value}"
                    
                    elif key in ['local_frame', 'odom_frame_id', 'odom_frame']:
                        if value == 'odom' and not value.startswith(f"{ns}/"):
                            data[key] = f"{ns}/{value}"
                    
                    elif key == 'global_frame':
                        if value == 'map' and not value.startswith(f"{ns}/"):
                            data[key] = f"{ns}/{value}"
                        elif value == 'odom' and not value.startswith(f"{ns}/"):
                            data[key] = f"{ns}/{value}"
                    
                    elif key.endswith('_topic') or key == 'topic':
                        if not value.startswith('/') and not value.startswith(f"{ns}/"):
                            data[key] = f"/{ns}/{value}"
                    
                    elif key in ['local_costmap_topic', 'local_footprint_topic', 
                               'global_costmap_topic', 'global_footprint_topic']:
                        if not value.startswith(f"{ns}/"):
                            data[key] = f"{ns}/{value}"
                
                apply_namespace(value, ns)
        elif isinstance(data, list):
            for item in data:
                apply_namespace(item, ns)

    apply_namespace(namespaced_params, namespace)
    
    output_path = f"/tmp/{namespace}_nav2_params.yaml"
    with open(output_path, 'w') as f:
        yaml.dump(namespaced_params, f, default_flow_style=False, sort_keys=False)
    
    print(f"Generated namespaced parameters for {namespace} at: {output_path}")
    
    return output_path

def generate_namespaced_slam_params(base_params_path, namespace):
    """
    Generate namespaced SLAM parameters for multi-robot setup.
    """
    with open(base_params_path, 'r') as f:
        template = yaml.safe_load(f)

    if 'slam_toolbox' not in template:
        raise ValueError(f"Template must contain 'slam_toolbox' key. Found keys: {list(template.keys())}")

    namespaced_params = {
        f"slam_toolbox_{namespace}": {
            'ros__parameters': dict(template['slam_toolbox']['ros__parameters'])
        }
    }
    
    params = namespaced_params[f"slam_toolbox_{namespace}"]['ros__parameters']
    
    params['odom_frame'] = f"{namespace}/{params['odom_frame']}"
    params['map_frame'] = f"{namespace}/{params['map_frame']}" 
    params['base_frame'] = f"{namespace}/{params['base_frame']}"
    params['scan_topic'] = f"/{namespace}/{params['scan_topic']}"
    
    output_path = os.path.join(tempfile.gettempdir(), f"{namespace}_slam_params.yaml")
    with open(output_path, 'w') as f:
        yaml.dump(namespaced_params, f, default_flow_style=False, sort_keys=False)

    print(f"Generated namespaced SLAM parameters for {namespace} at: {output_path}")
    
    return output_path
