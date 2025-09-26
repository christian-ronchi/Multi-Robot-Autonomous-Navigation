// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObject.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "dynamic_obstacle_detector_interfaces/msg/tracked_object.hpp"


#ifndef DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__BUILDER_HPP_
#define DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dynamic_obstacle_detector_interfaces
{

namespace msg
{

namespace builder
{

class Init_TrackedObject_covariance
{
public:
  explicit Init_TrackedObject_covariance(::dynamic_obstacle_detector_interfaces::msg::TrackedObject & msg)
  : msg_(msg)
  {}
  ::dynamic_obstacle_detector_interfaces::msg::TrackedObject covariance(::dynamic_obstacle_detector_interfaces::msg::TrackedObject::_covariance_type arg)
  {
    msg_.covariance = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dynamic_obstacle_detector_interfaces::msg::TrackedObject msg_;
};

class Init_TrackedObject_velocity
{
public:
  explicit Init_TrackedObject_velocity(::dynamic_obstacle_detector_interfaces::msg::TrackedObject & msg)
  : msg_(msg)
  {}
  Init_TrackedObject_covariance velocity(::dynamic_obstacle_detector_interfaces::msg::TrackedObject::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_TrackedObject_covariance(msg_);
  }

private:
  ::dynamic_obstacle_detector_interfaces::msg::TrackedObject msg_;
};

class Init_TrackedObject_position
{
public:
  explicit Init_TrackedObject_position(::dynamic_obstacle_detector_interfaces::msg::TrackedObject & msg)
  : msg_(msg)
  {}
  Init_TrackedObject_velocity position(::dynamic_obstacle_detector_interfaces::msg::TrackedObject::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_TrackedObject_velocity(msg_);
  }

private:
  ::dynamic_obstacle_detector_interfaces::msg::TrackedObject msg_;
};

class Init_TrackedObject_id
{
public:
  Init_TrackedObject_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TrackedObject_position id(::dynamic_obstacle_detector_interfaces::msg::TrackedObject::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_TrackedObject_position(msg_);
  }

private:
  ::dynamic_obstacle_detector_interfaces::msg::TrackedObject msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::dynamic_obstacle_detector_interfaces::msg::TrackedObject>()
{
  return dynamic_obstacle_detector_interfaces::msg::builder::Init_TrackedObject_id();
}

}  // namespace dynamic_obstacle_detector_interfaces

#endif  // DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__BUILDER_HPP_
