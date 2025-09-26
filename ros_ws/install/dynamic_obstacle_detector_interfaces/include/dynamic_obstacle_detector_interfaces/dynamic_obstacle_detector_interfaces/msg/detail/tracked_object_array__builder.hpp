// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "dynamic_obstacle_detector_interfaces/msg/tracked_object_array.hpp"


#ifndef DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT_ARRAY__BUILDER_HPP_
#define DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace dynamic_obstacle_detector_interfaces
{

namespace msg
{

namespace builder
{

class Init_TrackedObjectArray_objects
{
public:
  explicit Init_TrackedObjectArray_objects(::dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray & msg)
  : msg_(msg)
  {}
  ::dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray objects(::dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray::_objects_type arg)
  {
    msg_.objects = std::move(arg);
    return std::move(msg_);
  }

private:
  ::dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray msg_;
};

class Init_TrackedObjectArray_header
{
public:
  Init_TrackedObjectArray_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TrackedObjectArray_objects header(::dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_TrackedObjectArray_objects(msg_);
  }

private:
  ::dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray>()
{
  return dynamic_obstacle_detector_interfaces::msg::builder::Init_TrackedObjectArray_header();
}

}  // namespace dynamic_obstacle_detector_interfaces

#endif  // DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT_ARRAY__BUILDER_HPP_
