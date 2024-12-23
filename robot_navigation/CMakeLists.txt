cmake_minimum_required(VERSION 3.8)
project(robot_navigation)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)



install(
	PROGRAMS  script/waypoint_node.py
	DESTINATION lib/${PROJECT_NAME}/
	RENAME waypoint_node  )

	install(	
	 DIRECTORY map launch config rviz script
	 DESTINATION share/${PROJECT_NAME}/
)


ament_package()
