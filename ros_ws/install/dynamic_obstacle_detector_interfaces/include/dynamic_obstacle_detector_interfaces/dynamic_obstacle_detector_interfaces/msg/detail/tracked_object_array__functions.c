// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `objects`
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object__functions.h"

bool
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__init(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__fini(msg);
    return false;
  }
  // objects
  if (!dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__init(&msg->objects, 0)) {
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__fini(msg);
    return false;
  }
  return true;
}

void
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__fini(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // objects
  dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__fini(&msg->objects);
}

bool
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__are_equal(const dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray * lhs, const dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // objects
  if (!dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__are_equal(
      &(lhs->objects), &(rhs->objects)))
  {
    return false;
  }
  return true;
}

bool
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__copy(
  const dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray * input,
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // objects
  if (!dynamic_obstacle_detector_interfaces__msg__TrackedObject__Sequence__copy(
      &(input->objects), &(output->objects)))
  {
    return false;
  }
  return true;
}

dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray *
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray * msg = (dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray *)allocator.allocate(sizeof(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray));
  bool success = dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__destroy(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence__init(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray * data = NULL;

  if (size) {
    data = (dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray *)allocator.zero_allocate(size, sizeof(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__fini(&data[i - 1]);
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
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence__fini(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence * array)
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
      dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__fini(&array->data[i]);
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

dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence *
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence * array = (dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence *)allocator.allocate(sizeof(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence__destroy(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence__are_equal(const dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence * lhs, const dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence__copy(
  const dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence * input,
  dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray * data =
      (dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
