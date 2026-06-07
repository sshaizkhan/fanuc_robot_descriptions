#!/usr/bin/env python3
"""View a RoboDK-derived robot in RViz with a joint slider GUI.

  ros2 launch fanuc_robot_descriptions view_robot.launch.py
  ros2 launch fanuc_robot_descriptions view_robot.launch.py description_file:=<model>.urdf.xacro
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (Command, FindExecutable, LaunchConfiguration,
                                   PathJoinSubstitution)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = LaunchConfiguration("description_package")
    desc_file = LaunchConfiguration("description_file")
    prefix = LaunchConfiguration("prefix")
    robot_description = {"robot_description": Command([
        FindExecutable(name="xacro"), " ",
        PathJoinSubstitution([FindPackageShare(pkg), "urdf", desc_file]),
        " ", "prefix:=", prefix])}
    rviz = PathJoinSubstitution([FindPackageShare(pkg), "rviz", "view_robot.rviz"])
    return LaunchDescription([
        DeclareLaunchArgument("description_package", default_value="fanuc_robot_descriptions"),
        DeclareLaunchArgument("description_file", default_value="arc_mate_100id.urdf.xacro",
                              description="model file in urdf/ (e.g. arc_mate_100id.urdf.xacro)"),
        DeclareLaunchArgument("prefix", default_value=""),
        Node(package="robot_state_publisher", executable="robot_state_publisher",
             output="screen", parameters=[robot_description]),
        Node(package="joint_state_publisher_gui", executable="joint_state_publisher_gui",
             output="screen"),
        Node(package="rviz2", executable="rviz2", name="rviz2", output="screen",
             arguments=["-d", rviz]),
    ])
