// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObject.idl
// generated code does not contain a copyright notice

#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_dynamic_obstacle_detector_interfaces
const rosidl_type_hash_t *
dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x90, 0x20, 0x5f, 0x05, 0x92, 0xe6, 0x6b, 0x5f,
      0x62, 0x36, 0x21, 0x38, 0x81, 0x04, 0xc5, 0x28,
      0x8d, 0xcb, 0x23, 0xdd, 0x8b, 0x16, 0xe6, 0xf5,
      0x00, 0x64, 0x09, 0x18, 0xf1, 0x48, 0xab, 0xa1,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "geometry_msgs/msg/detail/vector3__functions.h"
#include "geometry_msgs/msg/detail/point__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t geometry_msgs__msg__Point__EXPECTED_HASH = {1, {
    0x69, 0x63, 0x08, 0x48, 0x42, 0xa9, 0xb0, 0x44,
    0x94, 0xd6, 0xb2, 0x94, 0x1d, 0x11, 0x44, 0x47,
    0x08, 0xd8, 0x92, 0xda, 0x2f, 0x4b, 0x09, 0x84,
    0x3b, 0x9c, 0x43, 0xf4, 0x2a, 0x7f, 0x68, 0x81,
  }};
static const rosidl_type_hash_t geometry_msgs__msg__Vector3__EXPECTED_HASH = {1, {
    0xcc, 0x12, 0xfe, 0x83, 0xe4, 0xc0, 0x27, 0x19,
    0xf1, 0xce, 0x80, 0x70, 0xbf, 0xd1, 0x4a, 0xec,
    0xd4, 0x0f, 0x75, 0xa9, 0x66, 0x96, 0xa6, 0x7a,
    0x2a, 0x1f, 0x37, 0xf7, 0xdb, 0xb0, 0x76, 0x5d,
  }};
#endif

static char dynamic_obstacle_detector_interfaces__msg__TrackedObject__TYPE_NAME[] = "dynamic_obstacle_detector_interfaces/msg/TrackedObject";
static char geometry_msgs__msg__Point__TYPE_NAME[] = "geometry_msgs/msg/Point";
static char geometry_msgs__msg__Vector3__TYPE_NAME[] = "geometry_msgs/msg/Vector3";

// Define type names, field names, and default values
static char dynamic_obstacle_detector_interfaces__msg__TrackedObject__FIELD_NAME__id[] = "id";
static char dynamic_obstacle_detector_interfaces__msg__TrackedObject__FIELD_NAME__position[] = "position";
static char dynamic_obstacle_detector_interfaces__msg__TrackedObject__FIELD_NAME__velocity[] = "velocity";
static char dynamic_obstacle_detector_interfaces__msg__TrackedObject__FIELD_NAME__covariance[] = "covariance";

static rosidl_runtime_c__type_description__Field dynamic_obstacle_detector_interfaces__msg__TrackedObject__FIELDS[] = {
  {
    {dynamic_obstacle_detector_interfaces__msg__TrackedObject__FIELD_NAME__id, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {dynamic_obstacle_detector_interfaces__msg__TrackedObject__FIELD_NAME__position, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    },
    {NULL, 0, 0},
  },
  {
    {dynamic_obstacle_detector_interfaces__msg__TrackedObject__FIELD_NAME__velocity, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {geometry_msgs__msg__Vector3__TYPE_NAME, 25, 25},
    },
    {NULL, 0, 0},
  },
  {
    {dynamic_obstacle_detector_interfaces__msg__TrackedObject__FIELD_NAME__covariance, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE_ARRAY,
      16,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription dynamic_obstacle_detector_interfaces__msg__TrackedObject__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Vector3__TYPE_NAME, 25, 25},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {dynamic_obstacle_detector_interfaces__msg__TrackedObject__TYPE_NAME, 54, 54},
      {dynamic_obstacle_detector_interfaces__msg__TrackedObject__FIELDS, 4, 4},
    },
    {dynamic_obstacle_detector_interfaces__msg__TrackedObject__REFERENCED_TYPE_DESCRIPTIONS, 2, 2},
  };
  if (!constructed) {
    assert(0 == memcmp(&geometry_msgs__msg__Point__EXPECTED_HASH, geometry_msgs__msg__Point__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = geometry_msgs__msg__Point__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Vector3__EXPECTED_HASH, geometry_msgs__msg__Vector3__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = geometry_msgs__msg__Vector3__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Rappresenta un singolo oggetto tracciato\n"
  "\n"
  "uint32 id                     # ID univoco dell'ostacolo\n"
  "\n"
  "geometry_msgs/Point position  # Posizione stimata (dal filtro di Kalman)\n"
  "geometry_msgs/Vector3 velocity # Velocit\\xc3\\xa0 stimata (dal filtro di Kalman)\n"
  "\n"
  "# Matrice di covarianza dello stato [x, y, vx, vy] 4x4\n"
  "# Rappresenta l'incertezza della stima.\n"
  "# Ordine: (x, y, vx, vy)\n"
  "# Row-major order.\n"
  "float64[16] covariance";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {dynamic_obstacle_detector_interfaces__msg__TrackedObject__TYPE_NAME, 54, 54},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 411, 411},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[3];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 3, 3};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_individual_type_description_source(NULL),
    sources[1] = *geometry_msgs__msg__Point__get_individual_type_description_source(NULL);
    sources[2] = *geometry_msgs__msg__Vector3__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
