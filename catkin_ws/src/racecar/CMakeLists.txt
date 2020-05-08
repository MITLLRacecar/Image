cmake_minimum_required(VERSION 2.8.3)
project(racecar)

find_package(catkin REQUIRED COMPONENTS
  ackermann_msgs
  sensor_msgs
  roscpp
  rospy
  std_msgs
)

catkin_package()

