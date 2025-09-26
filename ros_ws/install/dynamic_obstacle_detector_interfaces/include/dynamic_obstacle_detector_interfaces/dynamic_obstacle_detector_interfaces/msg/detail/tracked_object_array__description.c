// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice

#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_dynamic_obstacle_detector_interfaces
const rosidl_type_hash_t *
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x66, 0xb6, 0x92, 0xf5, 0xbe, 0xeb, 0xe5, 0xde,
      0x42, 0xd1, 0x2c, 0xcb, 0xe0, 0x15, 0x60, 0x45,
      0x96, 0xba, 0x84, 0xda, 0x79, 0x0a, 0x6a, 0xa6,
      0xaa, 0xe4, 0x22, 0x38, 0xc4, 0x3b, 0xd8, 0x12,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "std_msgs/msg/detail/header__functions.h"
#include "geometry_msgs/msg/detail/vector3__functions.h"
#include "geometry_msgs/msg/detail/point__functions.h"
#include "builtin_interfaces/msg/detail/time__functions.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t dynamic_obstacle_detector_interfaces__msg__TrackedObject__EXPECTED_HASH = {1, {
    0x90, 0x20, 0x5f, 0x05, 0x92, 0xe6, 0x6b, 0x5f,
    0x62, 0x36, 0x21, 0x38, 0x81, 0x04, 0xc5, 0x28,
    0x8d, 0xcb, 0x23, 0xdd, 0x8b, 0x16, 0xe6, 0xf5,
    0x00, 0x64, 0x09, 0x18, 0xf1, 0x48, 0xab, 0xa1,
  }};
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
static const rosidl_type_hash_t std_msgs__msg__Header__EXPECTED_HASH = {1, {
    0xf4, 0x9f, 0xb3, 0xae, 0x2c, 0xf0, 0x70, 0xf7,
    0x93, 0x64, 0x5f, 0xf7, 0x49, 0x68, 0x3a, 0xc6,
    0xb0, 0x62, 0x03, 0xe4, 0x1c, 0x89, 0x1e, 0x17,
    0x70, 0x1b, 0x1c, 0xb5, 0x97, 0xce, 0x6a, 0x01,
  }};
#endif

static char dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__TYPE_NAME[] = "dynamic_obstacle_detector_interfaces/msg/TrackedObjectArray";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char dynamic_obstacle_detector_interfaces__msg__TrackedObject__TYPE_NAME[] = "dynamic_obstacle_detector_interfaces/msg/TrackedObject";
static char geometry_msgs__msg__Point__TYPE_NAME[] = "geometry_msgs/msg/Point";
static char geometry_msgs__msg__Vector3__TYPE_NAME[] = "geometry_msgs/msg/Vector3";
static char std_msgs__msg__Header__TYPE_NAME[] = "std_msgs/msg/Header";

// Define type names, field names, and default values
static char dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__FIELD_NAME__header[] = "header";
static char dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__FIELD_NAME__objects[] = "objects";

static rosidl_runtime_c__type_description__Field dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__FIELDS[] = {
  {
    {dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__FIELD_NAME__header, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    },
    {NULL, 0, 0},
  },
  {
    {dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__FIELD_NAME__objects, 7, 7},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_UNBOUNDED_SEQUENCE,
      0,
      0,
      {dynamic_obstacle_detector_interfaces__msg__TrackedObject__TYPE_NAME, 54, 54},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {dynamic_obstacle_detector_interfaces__msg__TrackedObject__TYPE_NAME, 54, 54},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Point__TYPE_NAME, 23, 23},
    {NULL, 0, 0},
  },
  {
    {geometry_msgs__msg__Vector3__TYPE_NAME, 25, 25},
    {NULL, 0, 0},
  },
  {
    {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__TYPE_NAME, 59, 59},
      {dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__FIELDS, 2, 2},
    },
    {dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__REFERENCED_TYPE_DESCRIPTIONS, 5, 5},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&dynamic_obstacle_detector_interfaces__msg__TrackedObject__EXPECTED_HASH, dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Point__EXPECTED_HASH, geometry_msgs__msg__Point__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = geometry_msgs__msg__Point__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&geometry_msgs__msg__Vector3__EXPECTED_HASH, geometry_msgs__msg__Vector3__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = geometry_msgs__msg__Vector3__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&std_msgs__msg__Header__EXPECTED_HASH, std_msgs__msg__Header__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = std_msgs__msg__Header__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Rappresenta un array di oggetti tracciati, tipicamente da un singolo robot\n"
  "\n"
  "std_msgs/Header header  # Timestamp e frame_id della rilevazione\n"
  "\n"
  "TrackedObject[] objects # Lista degli oggetti tracciati";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__TYPE_NAME, 59, 59},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 200, 200},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[6];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 6, 6};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *dynamic_obstacle_detector_interfaces__msg__TrackedObject__get_individual_type_description_source(NULL);
    sources[3] = *geometry_msgs__msg__Point__get_individual_type_description_source(NULL);
    sources[4] = *geometry_msgs__msg__Vector3__get_individual_type_description_source(NULL);
    sources[5] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
