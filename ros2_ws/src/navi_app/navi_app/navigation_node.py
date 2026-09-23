import rclpy
from rclpy.node import Node

from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose

from geometry_msgs.msg import PoseStamped


class NavigationNode(Node):

    def __init__(self):
        super().__init__('navigation_node')

        self.action_client = ActionClient(
            self,
            NavigateToPose,
            '/navigate_to_pose'
        )

        self.get_logger().info('Navigation node started')

        self.send_goal()


    def send_goal(self):

        self.get_logger().info('Waiting for Nav2...')

        self.action_client.wait_for_server()

        self.get_logger().info('Nav2 is available')


        goal_msg = NavigateToPose.Goal()

        goal_msg.pose = PoseStamped()

        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()

        goal_msg.pose.pose.position.x = 2.61
        goal_msg.pose.pose.position.y = -1.43
        goal_msg.pose.pose.position.z = 0.0

        goal_msg.pose.pose.orientation.x = 0.0
        goal_msg.pose.pose.orientation.y = 0.0
        goal_msg.pose.pose.orientation.z = 0.0
        goal_msg.pose.pose.orientation.w = 1.0

        self.get_logger().info(
            'Sending navigation goal: x=2.61, y=-1.43'
        )

        self.send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self.send_goal_future.add_done_callback(
            self.goal_response_callback
        )


    def goal_response_callback(self, future):

        goal_handle = future.result()

        if not goal_handle.accepted:

            self.get_logger().error('Navigation goal rejected')

            return

        self.get_logger().info('Navigation goal accepted')

        self.get_result_future = goal_handle.get_result_async()

        self.get_result_future.add_done_callback(
            self.get_result_callback
        )


    def feedback_callback(self, feedback_msg):

        feedback = feedback_msg.feedback

        self.get_logger().info(
            f'Distance remaining: {feedback.distance_remaining:.2f} m' 
        )


    def get_result_callback(self, future):

        result = future.result().result

        self.get_logger().info(
            f'Navigation completed with result: {result}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = NavigationNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
