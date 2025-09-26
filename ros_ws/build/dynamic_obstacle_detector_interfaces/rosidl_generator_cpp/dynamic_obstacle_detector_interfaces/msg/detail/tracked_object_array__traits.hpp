// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "dynamic_obstacle_detector_interfaces/msg/tracked_object_array.hpp"


#ifndef DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT_ARRAY__TRAITS_HPP_
#define DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT_ARRAY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'objects'
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__traits.hpp"

namespace dynamic_obstacle_detector_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const TrackedObjectArray & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: objects
  {
    if (msg.objects.size() == 0) {
      out << "objects: []";
    } else {
      out << "objects: [";
      size_t pending_items = msg.objects.size();
      for (auto item : msg.objects) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TrackedObjectArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: objects
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.objects.size() == 0) {
      out << "objects: []\n";
    } else {
      out << "objects:\n";
      for (auto item : msg.objects) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TrackedObjectArray & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace dynamic_obstacle_detector_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use dynamic_obstacle_detector_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  dynamic_obstacle_detector_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use dynamic_obstacle_detector_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray & msg)
{
  return dynamic_obstacle_detector_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray>()
{
  return "dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray";
}

template<>
inline const char * name<dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray>()
{
  return "dynamic_obstacle_detector_interfaces/msg/TrackedObjectArray";
}

template<>
struct has_fixed_size<dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT_ARRAY__TRAITS_HPP_
