import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/tecnical/turtlebot-cicd/ros2_ws/install/navi_app'
