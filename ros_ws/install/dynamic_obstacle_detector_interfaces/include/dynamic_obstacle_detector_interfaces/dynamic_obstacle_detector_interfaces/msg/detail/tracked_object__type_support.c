// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObject.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__rosidl_typesupport_introspection_c.h"
#include "dynamic_obstacle_detector_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__functions.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__struct.h"


// Include directives for member types
// Member `position`
#include "geometry_msgs/msg/point.h"
// Member `position`
#include "geometry_msgs/msg/detail/point__rosidl_typesupport_introspection_c.h"
// Member `velocity`
#include "geometry_msgs/msg/vector3.h"
// Member `velocity`
#include "geometry_msgs/msg/detail/vector3__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__init(message_memory);
}

void dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_fini_function(void * message_memory)
{
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__fini(message_memory);
}

size_t dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__size_function__TrackedObject__covariance(
  const void * untyped_member)
{
  (void)untyped_member;
  return 16;
}

const void * dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__get_const_function__TrackedObject__covariance(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__get_function__TrackedObject__covariance(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__fetch_function__TrackedObject__covariance(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__get_const_function__TrackedObject__covariance(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__assign_function__TrackedObject__covariance(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__get_function__TrackedObject__covariance(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_member_array[4] = {
  {
    "id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamic_obstacle_detector_interfaces__msg__TrackedObject, id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamic_obstacle_detector_interfaces__msg__TrackedObject, position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamic_obstacle_detector_interfaces__msg__TrackedObject, velocity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "covariance",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is key
    true,  // is array
    16,  // array size
    false,  // is upper bound
    offsetof(dynamic_obstacle_detector_interfaces__msg__TrackedObject, covariance),  // bytes offset in struct
    NULL,  // default value
    dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__size_function__TrackedObject__covariance,  // size() function pointer
    dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__get_const_function__TrackedObject__covariance,  // get_const(index) function pointer
    dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__get_function__TrackedObject__covariance,  // get(index) function pointer
    dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__fetch_function__TrackedObject__covariance,  // fetch(index, &value) function pointer
    dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__assign_function__TrackedObject__covariance,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_members = {
  "dynamic_obstacle_detector_interfaces__msg",  // message namespace
  "TrackedObject",  // message name
  4,  // number of fields
  sizeof(dynamic_obstacle_detector_interfaces__msg__TrackedObject),
  false,  // has_any_key_member_
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_member_array,  // message members
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_init_function,  // function to initialize message memory (memory has to be allocated)
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_type_support_handle = {
  0,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_members,
  get_message_typesupport_handle_function,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_type_hash,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_type_description,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dynamic_obstacle_detector_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dynamic_obstacle_detector_interfaces, msg, TrackedObject)() {
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Vector3)();
  if (!dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_type_support_handle.typesupport_identifier) {
    dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dynamic_obstacle_detector_interfaces__msg__TrackedObject__rosidl_typesupport_introspection_c__TrackedObject_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
