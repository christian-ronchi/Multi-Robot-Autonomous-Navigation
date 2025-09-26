// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from dynamic_obstacle_detector_interfaces:msg/TrackedObjectArray.idl
// generated code does not contain a copyright notice
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__rosidl_typesupport_fastrtps_cpp.hpp"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__functions.h"
#include "dynamic_obstacle_detector_interfaces/msg/detail/tracked_object_array__struct.hpp"

#include <cstddef>
#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions
namespace std_msgs
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const std_msgs::msg::Header &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  std_msgs::msg::Header &);
size_t get_serialized_size(
  const std_msgs::msg::Header &,
  size_t current_alignment);
size_t
max_serialized_size_Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
bool cdr_serialize_key(
  const std_msgs::msg::Header &,
  eprosima::fastcdr::Cdr &);
size_t get_serialized_size_key(
  const std_msgs::msg::Header &,
  size_t current_alignment);
size_t
max_serialized_size_key_Header(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace std_msgs

namespace dynamic_obstacle_detector_interfaces
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const dynamic_obstacle_detector_interfaces::msg::TrackedObject &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  dynamic_obstacle_detector_interfaces::msg::TrackedObject &);
size_t get_serialized_size(
  const dynamic_obstacle_detector_interfaces::msg::TrackedObject &,
  size_t current_alignment);
size_t
max_serialized_size_TrackedObject(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
bool cdr_serialize_key(
  const dynamic_obstacle_detector_interfaces::msg::TrackedObject &,
  eprosima::fastcdr::Cdr &);
size_t get_serialized_size_key(
  const dynamic_obstacle_detector_interfaces::msg::TrackedObject &,
  size_t current_alignment);
size_t
max_serialized_size_key_TrackedObject(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace dynamic_obstacle_detector_interfaces


namespace dynamic_obstacle_detector_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{


bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dynamic_obstacle_detector_interfaces
cdr_serialize(
  const dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: header
  std_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.header,
    cdr);

  // Member: objects
  {
    size_t size = ros_message.objects.size();
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; i++) {
      dynamic_obstacle_detector_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize(
        ros_message.objects[i],
        cdr);
    }
  }

  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dynamic_obstacle_detector_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray & ros_message)
{
  // Member: header
  std_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.header);

  // Member: objects
  {
    uint32_t cdrSize;
    cdr >> cdrSize;
    size_t size = static_cast<size_t>(cdrSize);

    // Check there are at least 'size' remaining bytes in the CDR stream before resizing
    auto old_state = cdr.get_state();
    bool correct_size = cdr.jump(size);
    cdr.set_state(old_state);
    if (!correct_size) {
      fprintf(stderr, "sequence size exceeds remaining buffer\n");
      return false;
    }

    ros_message.objects.resize(size);
    for (size_t i = 0; i < size; i++) {
      dynamic_obstacle_detector_interfaces::msg::typesupport_fastrtps_cpp::cdr_deserialize(
        cdr, ros_message.objects[i]);
    }
  }

  return true;
}  // NOLINT(readability/fn_size)


size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dynamic_obstacle_detector_interfaces
get_serialized_size(
  const dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: header
  current_alignment +=
    std_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.header, current_alignment);

  // Member: objects
  {
    size_t array_size = ros_message.objects.size();
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment +=
        dynamic_obstacle_detector_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size(
        ros_message.objects[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}


size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dynamic_obstacle_detector_interfaces
max_serialized_size_TrackedObjectArray(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Member: header
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        std_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // Member: objects
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        dynamic_obstacle_detector_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_TrackedObject(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray;
    is_plain =
      (
      offsetof(DataType, objects) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dynamic_obstacle_detector_interfaces
cdr_serialize_key(
  const dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: header
  std_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize_key(
    ros_message.header,
    cdr);

  // Member: objects
  {
    size_t size = ros_message.objects.size();
    cdr << static_cast<uint32_t>(size);
    for (size_t i = 0; i < size; i++) {
      dynamic_obstacle_detector_interfaces::msg::typesupport_fastrtps_cpp::cdr_serialize_key(
        ros_message.objects[i],
        cdr);
    }
  }

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dynamic_obstacle_detector_interfaces
get_serialized_size_key(
  const dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: header
  current_alignment +=
    std_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size_key(
    ros_message.header, current_alignment);

  // Member: objects
  {
    size_t array_size = ros_message.objects.size();
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment +=
        dynamic_obstacle_detector_interfaces::msg::typesupport_fastrtps_cpp::get_serialized_size_key(
        ros_message.objects[index], current_alignment);
    }
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_dynamic_obstacle_detector_interfaces
max_serialized_size_key_TrackedObjectArray(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Member: header
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        std_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_key_Header(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: objects
  {
    size_t array_size = 0;
    full_bounded = false;
    is_plain = false;
    current_alignment += padding +
      eprosima::fastcdr::Cdr::alignment(current_alignment, padding);
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        dynamic_obstacle_detector_interfaces::msg::typesupport_fastrtps_cpp::max_serialized_size_key_TrackedObject(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray;
    is_plain =
      (
      offsetof(DataType, objects) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}


static bool _TrackedObjectArray__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _TrackedObjectArray__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _TrackedObjectArray__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _TrackedObjectArray__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_TrackedObjectArray(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _TrackedObjectArray__callbacks = {
  "dynamic_obstacle_detector_interfaces::msg",
  "TrackedObjectArray",
  _TrackedObjectArray__cdr_serialize,
  _TrackedObjectArray__cdr_deserialize,
  _TrackedObjectArray__get_serialized_size,
  _TrackedObjectArray__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _TrackedObjectArray__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_TrackedObjectArray__callbacks,
  get_message_typesupport_handle_function,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_hash,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_description,
  &dynamic_obstacle_detector_interfaces__msg__TrackedObjectArray__get_type_description_sources,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace dynamic_obstacle_detector_interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_dynamic_obstacle_detector_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<dynamic_obstacle_detector_interfaces::msg::TrackedObjectArray>()
{
  return &dynamic_obstacle_detector_interfaces::msg::typesupport_fastrtps_cpp::_TrackedObjectArray__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, dynamic_obstacle_detector_interfaces, msg, TrackedObjectArray)() {
  return &dynamic_obstacle_detector_interfaces::msg::typesupport_fastrtps_cpp::_TrackedObjectArray__handle;
}

#ifdef __cplusplus
}
#endif
