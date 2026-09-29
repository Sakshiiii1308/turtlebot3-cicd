FROM ros:humble-ros-base-jammy

SHELL ["/bin/bash", "-c"]

ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV ROS_DOMAIN_ID=0

WORKDIR /ros2_ws

COPY ros2_ws/src/ ./src/

RUN apt-get update && \
    apt-get install -y ros-humble-rmw-cyclonedds-cpp && \
    rosdep update && \
    rosdep install --from-paths src \
     --ignore-src -r -y && \
    rm -rf /var/lib/apt/lists/*

RUN source /opt/ros/humble/setup.bash && \
    colcon build --packages-select navi_app

CMD ["bash", "-c", "source /opt/ros/humble/setup.bash && source /ros2_ws/install/setup.bash && ros2 run navi_app navigation_node"]
