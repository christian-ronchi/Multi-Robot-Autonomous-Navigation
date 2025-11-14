#ifndef OBSTACLE_FUSION_LAYER_HPP_
#define OBSTACLE_FUSION_LAYER_HPP_

#include "nav2_costmap_2d/layer.hpp"
#include "nav2_costmap_2d/layered_costmap.hpp"
#include "dynamic_obstacle_detector_interfaces/msg/tracked_object_array.hpp"
#include "geometry_msgs/msg/point.hpp"
#include "rclcpp/rclcpp.hpp"
#include <string>
#include <vector>
#include <mutex>

namespace obstacle_fusion_layer
{

class ObstacleFusionLayer : public nav2_costmap_2d::Layer
{
public:
  ObstacleFusionLayer();
  virtual ~ObstacleFusionLayer();

  void onInitialize() override;
  void updateBounds(
    double robot_x, double robot_y, double robot_yaw, double * min_x,
    double * min_y, double * max_x, double * max_y) override;
  void updateCosts(
    nav2_costmap_2d::Costmap2D & master_grid,
    int min_i, int min_j, int max_i, int max_j) override;
  void reset() override;
  void onFootprintChanged() override;
  bool isClearable() override { return false; }

private:
  void obstaclesCallback(const dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray::SharedPtr msg);
  void drawObstacle(
    nav2_costmap_2d::Costmap2D & costmap, 
    double x, double y, double inflation_radius);

  rclcpp::Subscription<dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray>::SharedPtr sub_;
  std::vector<dynamic_obstacle_detector_interfaces::msg::TrackedObject> obstacles_;
  double inflation_radius_;
  bool enabled_;
  std::mutex mutex_;
  
  // Internal flags to manage update state independently of Nav2 base class implementation
  bool need_recalculation_ = false;
  bool current_ = false;
};

}  // namespace obstacle_fusion_layer

#endif  // OBSTACLE_FUSION_LAYER_HPP_