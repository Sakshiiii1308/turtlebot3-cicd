import unittest

from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose


class TestNavigationGoal(unittest.TestCase):

    def test_goal_position(self):

        goal_msg = NavigateToPose.Goal()

        goal_msg.pose = PoseStamped()

        goal_msg.pose.header.frame_id = 'map'

        goal_msg.pose.pose.position.x = 3.62
        goal_msg.pose.pose.position.y = 1.04
        goal_msg.pose.pose.position.z = 0.0

        self.assertEqual(
            goal_msg.pose.header.frame_id,
            'map'
        )

        self.assertEqual(
            goal_msg.pose.pose.position.x,
            3.62
        )

        self.assertEqual(
            goal_msg.pose.pose.position.y,
            1.04
        )

        self.assertEqual(
            goal_msg.pose.pose.position.z,
            0.0
        )


if __name__ == '__main__':
    unittest.main()
