#!/usr/bin/env  python3

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from rclpy.node import Node

class NavigatorNode(Node):
    def __init__(self):
        super().__init__('navigator_node')
        self.navigator = BasicNavigator()

    def set_initial_pose(self):
        initial_pose = PoseStamped()
        initial_pose.header.frame_id = 'map'
        initial_pose.header.stamp = self.navigator.get_clock().now().to_msg()
        initial_pose.pose.position.x = 0.0
        initial_pose.pose.position.y = 0.0
        initial_pose.pose.orientation.z = 0.0
        initial_pose.pose.orientation.w = 1.0 
        self.navigator.setInitialPose(initial_pose)

    def navigate(self):
        self.navigator.waitUntilNav2Active()

        waypoints = []
        goal_pose1 = PoseStamped()
        goal_pose1.header.frame_id = 'map'
        goal_pose1.pose.position.x = 3.83
        goal_pose1.pose.position.y = -8.88
        goal_pose1.pose.orientation.w = 0.707
        goal_pose1.pose.orientation.z = 0.807
        waypoints.append(goal_pose1)

        goal_pose2 = PoseStamped()
        goal_pose2.header.frame_id = 'map'
        goal_pose2.pose.position.x = 1.18
        goal_pose2.pose.position.y = 7.2
        goal_pose2.pose.orientation.w = 0.707
        goal_pose2.pose.orientation.z = 0.807
        waypoints.append(goal_pose2)

        goal_pose3 = PoseStamped()
        goal_pose3.header.frame_id = 'map'
        goal_pose3.pose.position.x = -6.0
        goal_pose3.pose.position.y = 9.3
        goal_pose3.pose.orientation.w = 0.707
        goal_pose3.pose.orientation.z = 0.807
        waypoints.append(goal_pose3)

        for i, waypoint in enumerate(waypoints):
            self.get_logger().info(f"Navigating to waypoint {i + 1}...")
            self.navigator.goToPose(waypoint)

            while not self.navigator.isTaskComplete():
                feedback = self.navigator.getFeedback()
                if feedback:
                    self.get_logger().info(f"Moving towards waypoint {i + 1}...")

            result = self.navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                self.get_logger().info(f"Reached waypoint {i + 1}!")
            elif result == TaskResult.CANCELED:
                self.get_logger().warn("Navigation canceled. Exiting...")
                break
            elif result == TaskResult.FAILED:
                self.get_logger().error("Failed to reach waypoint. Exiting...")
                break

        self.get_logger().info("All waypoints completed!")


def main():
    rclpy.init()
    node = NavigatorNode()
    try:
        node.set_initial_pose()
        node.navigate()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
