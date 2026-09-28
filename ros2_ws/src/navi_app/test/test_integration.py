import unittest
import rclpy

from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose


class TestNavigationIntegration(unittest.TestCase):

    def setUp(self):
        rclpy.init()

        self.node = rclpy.create_node(
                'navigation_integration_test'
        )

        self.action_client = ActionClient(
                self.node,
                NavigateToPose,
                '/navigate_to_pose'
        )

    def test_nav2_connection(self):

        available = self.action_client.wait_for_server(
                timeout_sec=10.0
        )

        self.assertTrue(
                available,
                'Nav2 action server is not available'
        )

    def test_navigation_goal_accepted(self):

        available = self.action_client.wait_for_server(
            timeout_sec=10.0
        )

        self.assertTrue(
                available,
                'Nav2 action server is not available'
        )

        goal = NavigateToPose.Goal()

        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.node.get_clock().now().to_msg()

        goal.pose.pose.position.x = 1.1
        goal.pose.pose.position.y = 0.9
        goal.pose.pose.orientation.w = 0.0

        future = self.action_client.send_goal_async(goal)

        rclpy.spin_until_future_complete(
             self.node,
             future,
             timeout_sec=10.0
        )

        self.assertTrue(future.done())

        goal_handle = future.result()

        self.assertTrue(goal_handle.accepted)

        cancel_future = goal_handle.cancel_goal_async()

        rclpy.spin_until_future_complete(
            self.node,
            cancel_future,
            timeout_sec=10.0
        )

        self.assertTrue(cancel_future.done())

    def tearDown(self):

        self.node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    unittest.main()
