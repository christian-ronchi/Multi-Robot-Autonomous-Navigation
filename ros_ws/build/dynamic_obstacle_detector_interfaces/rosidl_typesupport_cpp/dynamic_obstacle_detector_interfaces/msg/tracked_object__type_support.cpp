// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObject.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__functions.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace dynamic_obstacle_detector_interfaces
{

namespace msg
{

namespace rosidl_typesupport_cpp
{

typedef struct _TrackedObject_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _TrackedObject_type_support_ids_t;

static const _TrackedObject_type_support_ids_t _TrackedObject_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _TrackedObject_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _TrackedObject_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _TrackedObject_type_support_symbol_names_t _TrackedObject_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, dynamic_obstacle_detector_interfaces, msg, TrackedObject)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, dynamic_obstacle_detector_interfaces, msg, TrackedObject)),
  }
};

typedef struct _TrackedObject_type_support_data_t
{
  void * data[2];
} _TrackedObject_type_support_data_t;

static _TrackedObject_type_support_data_t _TrackedObject_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _TrackedObject_message_typesupport_map = {
  2,
  "dynamic_obstacle_detector_interfaces",
  &_TrackedObject_message_typesupport_ids.typesupport_identifier[0],
  &_TrackedObject_message_typesupport_symbol_names.symbol_name[0],
  &_TrackedObject_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t TrackedObject_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_TrackedObject_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_type_hash,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_type_description,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace msg

}  // namespace dynamic_obstacle_detector_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<dynamic_obstacle_detector_interfaces::msg::TrackedObject>()
{
  return &::dynamic_obstacle_detector_interfaces::msg::rosidl_typesupport_cpp::TrackedObject_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, dynamic_obstacle_detector_interfaces, msg, TrackedObject)() {
  return get_message_type_support_handle<dynamic_obstacle_detector_interfaces::msg::TrackedObject>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp
