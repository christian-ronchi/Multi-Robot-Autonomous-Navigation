// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__struct.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__type_support.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace dynamic_obstacle_detector_interfaces
{

namespace msg
{

namespace rosidl_typesupport_c
{

typedef struct _TrackedObjectArray_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _TrackedObjectArray_type_support_ids_t;

static const _TrackedObjectArray_type_support_ids_t _TrackedObjectArray_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _TrackedObjectArray_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _TrackedObjectArray_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _TrackedObjectArray_type_support_symbol_names_t _TrackedObjectArray_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, dynamic_obstacle_detector_interfaces, msg, TrackedObjectArray)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, dynamic_obstacle_detector_interfaces, msg, TrackedObjectArray)),
  }
};

typedef struct _TrackedObjectArray_type_support_data_t
{
  void * data[2];
} _TrackedObjectArray_type_support_data_t;

static _TrackedObjectArray_type_support_data_t _TrackedObjectArray_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _TrackedObjectArray_message_typesupport_map = {
  2,
  "dynamic_obstacle_detector_interfaces",
  &_TrackedObjectArray_message_typesupport_ids.typesupport_identifier[0],
  &_TrackedObjectArray_message_typesupport_symbol_names.symbol_name[0],
  &_TrackedObjectArray_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t TrackedObjectArray_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_TrackedObjectArray_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_hash,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_description,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace msg

}  // namespace dynamic_obstacle_detector_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, dynamic_obstacle_detector_interfaces, msg, TrackedObjectArray)() {
  return &::dynamic_obstacle_detector_interfaces::msg::rosidl_typesupport_c::TrackedObjectArray_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
