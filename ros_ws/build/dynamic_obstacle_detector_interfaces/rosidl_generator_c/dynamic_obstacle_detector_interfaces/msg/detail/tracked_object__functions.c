// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObject.idl
// generated code does not contain a copyright notice
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `position`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `velocity`
#include "geometry_msgs/msg/detail/vector3__functions.h"

bool
dynamic_obstacle_detector_interfaces__msg__TrackedObject__init(dynamic_obstacle_detector_interfaces__msg__TrackedObject * msg)
{
  if (!msg) {
    return false;
  }
  // id
  // position
  if (!geometry_msgs__msg__Point__init(&msg->position)) {
    dynamic_obstacle_detector_interfaces__msg__TrackedObject__fini(msg);
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Vector3__init(&msg->velocity)) {
    dynamic_obstacle_detector_interfaces__msg__TrackedObject__fini(msg);
    return false;
  }
  // covariance
  return true;
}

void
dynamic_obstacle_detector_interfaces__msg__TrackedObject__fini(dynamic_obstacle_detector_interfaces__msg__TrackedObject * msg)
{
  if (!msg) {
    return;
  }
  // id
  // position
  geometry_msgs__msg__Point__fini(&msg->position);
  // velocity
  geometry_msgs__msg__Vector3__fini(&msg->velocity);
  // covariance
}

bool
dynamic_obstacle_detector_interfaces__msg__TrackedObject__are_equal(const dynamic_obstacle_detector_interfaces__msg__TrackedObject * lhs, const dynamic_obstacle_detector_interfaces__msg__TrackedObject * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // position
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->position), &(rhs->position)))
  {
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Vector3__are_equal(
      &(lhs->velocity), &(rhs->velocity)))
  {
    return false;
  }
  // covariance
  for (size_t i = 0; i < 16; ++i) {
    if (lhs->covariance[i] != rhs->covariance[i]) {
      return false;
    }
  }
  return true;
}

bool
dynamic_obstacle_detector_interfaces__msg__TrackedObject__copy(
  const dynamic_obstacle_detector_interfaces__msg__TrackedObject * input,
  dynamic_obstacle_detector_interfaces__msg__TrackedObject * output)
{
  if (!input || !output) {
    return false;
  }
  // id
  output->id = input->id;
  // position
  if (!geometry_msgs__msg__Point__copy(
      &(input->position), &(output->position)))
  {
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Vector3__copy(
      &(input->velocity), &(output->velocity)))
  {
    return false;
  }
  // covariance
  for (size_t i = 0; i < 16; ++i) {
    output->covariance[i] = input->covariance[i];
  }
  return true;
}

dynamic_obstacle_detector_interfaces__msg__TrackedObject *
dynamic_obstacle_detector_interfaces__msg__TrackedObject__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dynamic_obstacle_detector_interfaces__msg__TrackedObject * msg = (dynamic_obstacle_detector_interfaces__msg__TrackedObject *)allocator.allocate(sizeof(dynamic_obstacle_detector_interfaces__msg__TrackedObject), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dynamic_obstacle_detector_interfaces__msg__TrackedObject));
  bool success = dynamic_obstacle_detector_interfaces__msg__TrackedObject__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dynamic_obstacle_detector_interfaces__msg__TrackedObject__destroy(dynamic_obstacle_detector_interfaces__msg__TrackedObject * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dynamic_obstacle_detector_interfaces__msg__TrackedObject__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__init(dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dynamic_obstacle_detector_interfaces__msg__TrackedObject * data = NULL;

  if (size) {
    data = (dynamic_obstacle_detector_interfaces__msg__TrackedObject *)allocator.zero_allocate(size, sizeof(dynamic_obstacle_detector_interfaces__msg__TrackedObject), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dynamic_obstacle_detector_interfaces__msg__TrackedObject__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dynamic_obstacle_detector_interfaces__msg__TrackedObject__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__fini(dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      dynamic_obstacle_detector_interfaces__msg__TrackedObject__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence *
dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence * array = (dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence *)allocator.allocate(sizeof(dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__destroy(dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__are_equal(const dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence * lhs, const dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dynamic_obstacle_detector_interfaces__msg__TrackedObject__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__copy(
  const dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence * input,
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dynamic_obstacle_detector_interfaces__msg__TrackedObject);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dynamic_obstacle_detector_interfaces__msg__TrackedObject * data =
      (dynamic_obstacle_detector_interfaces__msg__TrackedObject *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dynamic_obstacle_detector_interfaces__msg__TrackedObject__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dynamic_obstacle_detector_interfaces__msg__TrackedObject__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dynamic_obstacle_detector_interfaces__msg__TrackedObject__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
