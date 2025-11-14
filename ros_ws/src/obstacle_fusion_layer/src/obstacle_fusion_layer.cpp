#include "obstacle_fusion_layer/obstacle_fusion_layer.hpp"
#include "pluginlib/class_list_macros.hpp"
#include <algorithm>
#include <limits>

PLUGINLIB_EXPORT_CLASS(obstacle_fusion_layer::ObstacleFusionLayer, nav2_costmap_2d::Layer)

namespace obstacle_fusion_layer
{

using nav2_costmap_2d::LETHAL_OBSTACLE;
using nav2_costmap_2d::INSCRIBED_INFLATED_OBSTACLE;
using nav2_costmap_2d::NO_INFORMATION;

ObstacleFusionLayer::ObstacleFusionLayer()
{
}

ObstacleFusionLayer::~ObstacleFusionLayer()
{
}

void ObstacleFusionLayer::onInitialize()
{
  RCLCPP_INFO(logger_, "Initializing ObstacleFusionLayer...");

  declareParameter("enabled", rclcpp::ParameterValue(true));
  declareParameter("inflation_radius", rclcpp::ParameterValue(0.5));

  // SOLUTION: Use .lock() to convert WeakPtr to SharedPtr
  auto node = node_.lock();
  if (!node) {
    RCLCPP_ERROR(logger_, "Unable to acquire node pointer!");
    return;
  }

  node->get_parameter(name_ + ".enabled", enabled_);
  node->get_parameter(name_ + ".inflation_radius", inflation_radius_);

  sub_ = node->create_subscription<dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray>(
    "/global_tracked_obstacles",
    rclcpp::QoS(rclcpp::KeepLast(10)).best_effort().durability_volatile(),
    std::bind(&ObstacleFusionLayer::obstaclesCallback, this, std::placeholders::_1));

  RCLCPP_INFO(logger_, "ObstacleFusionLayer initialized with inflation_radius: %.2f m", inflation_radius_);
}

void ObstacleFusionLayer::obstaclesCallback(const dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray::SharedPtr msg)
{
  if (!enabled_) {
    return;
  }

  std::lock_guard<std::mutex> lock(mutex_);
  
  obstacles_.clear();
  for (const auto & obj : msg->objects) {
    if (obj.id >= 0) {
      obstacles_.push_back(obj);
    }
  }

  // SOLUTION: Use internal flags instead of base class flags
  need_recalculation_ = true;
  current_ = true;
}

void ObstacleFusionLayer::updateBounds(
  double robot_x, double robot_y, double robot_yaw, double * min_x,
  double * min_y, double * max_x, double * max_y)
{
  if (!enabled_ || !current_ || obstacles_.empty()) {
    // IF THERE ARE NO OBSTACLES, DO NOT MODIFY THE BOUNDS
    // Return the current bounds without modifying them
    return;
  }

  std::lock_guard<std::mutex> lock(mutex_);

  // Initialize with extreme values (inverse of typical usage)
  double min_x_local = std::numeric_limits<double>::max();
  double min_y_local = std::numeric_limits<double>::max();
  double max_x_local = std::numeric_limits<double>::lowest();
  double max_y_local = std::numeric_limits<double>::lowest();

  // Calculate bounds for all obstacles
  for (const auto & obj : obstacles_) {
    min_x_local = std::min(min_x_local, obj.position.x - inflation_radius_);
    min_y_local = std::min(min_y_local, obj.position.y - inflation_radius_);
    max_x_local = std::max(max_x_local, obj.position.x + inflation_radius_);
    max_y_local = std::max(max_y_local, obj.position.y + inflation_radius_);
  }

  // EXPAND bounds (never reduce them)
  *min_x = std::min(*min_x, min_x_local);
  *min_y = std::min(*min_y, min_y_local);
  *max_x = std::max(*max_x, max_x_local);
  *max_y = std::max(*max_y, max_y_local);
}

void ObstacleFusionLayer::updateCosts(
  nav2_costmap_2d::Costmap2D & master_grid,
  int min_i, int min_j, int max_i, int max_j)
{
  if (!enabled_ || !current_ || obstacles_.empty()) {
    return;
  }

  std::lock_guard<std::mutex> lock(mutex_);

  for (const auto & obj : obstacles_) {
    drawObstacle(master_grid, obj.position.x, obj.position.y, inflation_radius_);
  }

  need_recalculation_ = false; // Reset after update
}

void ObstacleFusionLayer::drawObstacle(
  nav2_costmap_2d::Costmap2D & costmap, 
  double x, double y, double inflation_radius)
{
  unsigned int mx, my;
  if (!costmap.worldToMap(x, y, mx, my)) {
    return;
  }

  // DRAW ONLY THE CENTRAL CELL AS LETHAL (254)
  // Actual inflation is handled by Nav2's InflationLayer
  costmap.setCost(mx, my, LETHAL_OBSTACLE);
}

void ObstacleFusionLayer::reset()
{
  std::lock_guard<std::mutex> lock(mutex_);
  obstacles_.clear();
  need_recalculation_ = false;  // Do not force recalculation if empty
  current_ = false;
}

void ObstacleFusionLayer::onFootprintChanged()
{
  need_recalculation_ = true;
}

}  // namespace obstacle_fusion_layer