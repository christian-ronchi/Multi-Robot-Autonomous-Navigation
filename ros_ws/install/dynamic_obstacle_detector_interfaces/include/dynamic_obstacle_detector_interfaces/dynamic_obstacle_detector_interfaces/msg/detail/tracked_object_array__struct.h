// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "dynamic_obstacle_detector_interfaces/msg/tracked_object_array.h"


#ifndef DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT_ARRAY__STRUCT_H_
#define DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'objects'
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__struct.h"

/// Struct defined in msg/TrackedObjectArray in the package dynamic_obstacle_detector_interfaces.
/**
  * Rappresenta un array di oggetti tracciati, tipicamente da un singolo robot
 */
typedef struct dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray
{
  /// Timestamp e frame_id della rilevazione
  std_msgs__msg__Header header;
  /// Lista degli oggetti tracciati
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence objects;
} dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray;

// Struct for a sequence of dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray.
typedef struct dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence
{
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT_ARRAY__STRUCT_H_
