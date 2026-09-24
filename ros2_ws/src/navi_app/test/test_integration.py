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

    def tearDown(self):

        self.node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    unittest.main()
