cmake_minimum_required(VERSION 3.5)
project(obstacle_fusion_layer)

# Trova i pacchetti necessari
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(nav2_costmap_2d REQUIRED)
find_package(pluginlib REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(dynamic_obstacle_detector_interfaces REQUIRED)

# Includi le cartelle di intestazione
include_directories(
  include
  ${nav2_costmap_2d_INCLUDE_DIRS}
  ${pluginlib_INCLUDE_DIRS}
  ${geometry_msgs_INCLUDE_DIRS}
  ${dynamic_obstacle_detector_interfaces_INCLUDE_DIRS}
)

# Compila la libreria del plugin
add_library(obstacle_fusion_layer SHARED
  src/obstacle_fusion_layer.cpp
)

# Linka le librerie
ament_target_dependencies(obstacle_fusion_layer
  rclcpp
  nav2_costmap_2d
  pluginlib
  geometry_msgs
  dynamic_obstacle_detector_interfaces
)

# Esporta il plugin
pluginlib_export_plugin_description_file(nav2_costmap_2d plugins.xml)

# Installa le intestazioni
install(DIRECTORY include/
  DESTINATION include
)

# Installa la libreria
install(TARGETS obstacle_fusion_layer
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

# Installa il file di descrizione del plugin
install(FILES plugins.xml
  DESTINATION share/${PROJECT_NAME}
)

# Generazione del pacchetto
ament_package()