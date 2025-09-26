// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__functions.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace dynamic_obstacle_detector_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void TrackedObjectArray_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray(_init);
}

void TrackedObjectArray_fini_function(void * message_memory)
{
  auto typed_message = static_cast<dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray *>(message_memory);
  typed_message->~TrackedObjectArray();
}

size_t size_function__TrackedObjectArray__objects(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<dynamic_obstacle_detector_interfaces::msg::TrackedObject> *>(untyped_member);
  return member->size();
}

const void * get_const_function__TrackedObjectArray__objects(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<dynamic_obstacle_detector_interfaces::msg::TrackedObject> *>(untyped_member);
  return &member[index];
}

void * get_function__TrackedObjectArray__objects(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<dynamic_obstacle_detector_interfaces::msg::TrackedObject> *>(untyped_member);
  return &member[index];
}

void fetch_function__TrackedObjectArray__objects(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const dynamic_obstacle_detector_interfaces::msg::TrackedObject *>(
    get_const_function__TrackedObjectArray__objects(untyped_member, index));
  auto & value = *reinterpret_cast<dynamic_obstacle_detector_interfaces::msg::TrackedObject *>(untyped_value);
  value = item;
}

void assign_function__TrackedObjectArray__objects(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<dynamic_obstacle_detector_interfaces::msg::TrackedObject *>(
    get_function__TrackedObjectArray__objects(untyped_member, index));
  const auto & value = *reinterpret_cast<const dynamic_obstacle_detector_interfaces::msg::TrackedObject *>(untyped_value);
  item = value;
}

void resize_function__TrackedObjectArray__objects(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<dynamic_obstacle_detector_interfaces::msg::TrackedObject> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember TrackedObjectArray_message_member_array[2] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "objects",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<dynamic_obstacle_detector_interfaces::msg::TrackedObject>(),  // members of sub message
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray, objects),  // bytes offset in struct
    nullptr,  // default value
    size_function__TrackedObjectArray__objects,  // size() function pointer
    get_const_function__TrackedObjectArray__objects,  // get_const(index) function pointer
    get_function__TrackedObjectArray__objects,  // get(index) function pointer
    fetch_function__TrackedObjectArray__objects,  // fetch(index, &value) function pointer
    assign_function__TrackedObjectArray__objects,  // assign(index, value) function pointer
    resize_function__TrackedObjectArray__objects  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers TrackedObjectArray_message_members = {
  "dynamic_obstacle_detector_interfaces::msg",  // message namespace
  "TrackedObjectArray",  // message name
  2,  // number of fields
  sizeof(dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray),
  false,  // has_any_key_member_
  TrackedObjectArray_message_member_array,  // message members
  TrackedObjectArray_init_function,  // function to initialize message memory (memory has to be allocated)
  TrackedObjectArray_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t TrackedObjectArray_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &TrackedObjectArray_message_members,
  get_message_typesupport_handle_function,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_hash,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_description,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace dynamic_obstacle_detector_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray>()
{
  return &::dynamic_obstacle_detector_interfaces::msg::rosidl_typesupport_introspection_cpp::TrackedObjectArray_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, dynamic_obstacle_detector_interfaces, msg, TrackedObjectArray)() {
  return &::dynamic_obstacle_detector_interfaces::msg::rosidl_typesupport_introspection_cpp::TrackedObjectArray_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
