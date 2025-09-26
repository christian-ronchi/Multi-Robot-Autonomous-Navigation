// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__rosidl_typesupport_introspection_c.h"
#include "dynamic_obstacle_detector_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__functions.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `objects`
#include "dynamic_obstacle_detector_interfaces/msg/tracked_object.h"
// Member `objects`
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__init(message_memory);
}

void dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_fini_function(void * message_memory)
{
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__fini(message_memory);
}

size_t dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__size_function__TrackedObjectArray__objects(
  const void * untyped_member)
{
  const dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence * member =
    (const dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence *)(untyped_member);
  return member->size;
}

const void * dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__get_const_function__TrackedObjectArray__objects(
  const void * untyped_member, size_t index)
{
  const dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence * member =
    (const dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence *)(untyped_member);
  return &member->data[index];
}

void * dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__get_function__TrackedObjectArray__objects(
  void * untyped_member, size_t index)
{
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence * member =
    (dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence *)(untyped_member);
  return &member->data[index];
}

void dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__fetch_function__TrackedObjectArray__objects(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const dynamic_obstacle_detector_interfaces__msg__TrackedObject * item =
    ((const dynamic_obstacle_detector_interfaces__msg__TrackedObject *)
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__get_const_function__TrackedObjectArray__objects(untyped_member, index));
  dynamic_obstacle_detector_interfaces__msg__TrackedObject * value =
    (dynamic_obstacle_detector_interfaces__msg__TrackedObject *)(untyped_value);
  *value = *item;
}

void dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__assign_function__TrackedObjectArray__objects(
  void * untyped_member, size_t index, const void * untyped_value)
{
  dynamic_obstacle_detector_interfaces__msg__TrackedObject * item =
    ((dynamic_obstacle_detector_interfaces__msg__TrackedObject *)
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__get_function__TrackedObjectArray__objects(untyped_member, index));
  const dynamic_obstacle_detector_interfaces__msg__TrackedObject * value =
    (const dynamic_obstacle_detector_interfaces__msg__TrackedObject *)(untyped_value);
  *item = *value;
}

bool dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__resize_function__TrackedObjectArray__objects(
  void * untyped_member, size_t size)
{
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence * member =
    (dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence *)(untyped_member);
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__fini(member);
  return dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_message_member_array[2] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "objects",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is key
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray, objects),  // bytes offset in struct
    NULL,  // default value
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__size_function__TrackedObjectArray__objects,  // size() function pointer
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__get_const_function__TrackedObjectArray__objects,  // get_const(index) function pointer
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__get_function__TrackedObjectArray__objects,  // get(index) function pointer
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__fetch_function__TrackedObjectArray__objects,  // fetch(index, &value) function pointer
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__assign_function__TrackedObjectArray__objects,  // assign(index, value) function pointer
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__resize_function__TrackedObjectArray__objects  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_message_members = {
  "dynamic_obstacle_detector_interfaces__msg",  // message namespace
  "TrackedObjectArray",  // message name
  2,  // number of fields
  sizeof(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray),
  false,  // has_any_key_member_
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_message_member_array,  // message members
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_init_function,  // function to initialize message memory (memory has to be allocated)
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_message_type_support_handle = {
  0,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_message_members,
  get_message_typesupport_handle_function,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_hash,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_description,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_description_sources,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_dynamic_obstacle_detector_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dynamic_obstacle_detector_interfaces, msg, TrackedObjectArray)() {
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dynamic_obstacle_detector_interfaces, msg, TrackedObject)();
  if (!dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_message_type_support_handle.typesupport_identifier) {
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__rosidl_typesupport_introspection_c__TrackedObjectArray_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
