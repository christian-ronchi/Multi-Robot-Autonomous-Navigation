// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObject.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "dynamic_obstacle_detector_interfaces/msg/tracked_object.h"


#ifndef DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__STRUCT_H_
#define DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'position'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'velocity'
#include "geometry_msgs/msg/detail/vector3__struct.h"

/// Struct defined in msg/TrackedObject in the package dynamic_obstacle_detector_interfaces.
/**
  * Rappresenta un singolo oggetto tracciato
 */
typedef struct dynamic_obstacle_detector_interfaces__msg__TrackedObject
{
  /// ID univoco dell'ostacolo
  uint32_t id;
  /// Posizione stimata (dal filtro di Kalman)
  geometry_msgs__msg__Point position;
  /// Velocità stimata (dal filtro di Kalman)
  geometry_msgs__msg__Vector3 velocity;
  /// Matrice di covarianza dello stato [x, y, vx, vy] 4x4
  /// Rappresenta l'incertezza della stima.
  /// Ordine: (x, y, vx, vy)
  /// Row-major order.
  double covariance[16];
} dynamic_obstacle_detector_interfaces__msg__TrackedObject;

// Struct for a sequence of dynamic_obstacle_detector_interfaces__msg__TrackedObject.
typedef struct dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence
{
  dynamic_obstacle_detector_interfaces__msg__TrackedObject * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DYNAMIC_OBSTACLE_DETECTOR_INTERFACES__MSG__DETAIL__TRACKED_OBJECT__STRUCT_H_
