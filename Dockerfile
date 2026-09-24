FROM ros:humble-ros-base-jammy

SHELL ["/bin/bash", "-c"]

WORKDIR /ros2_ws

COPY ros2_ws/src/ ./src/

RUN apt-get update && \
    rosdep update && \
    rosdep install --from-paths src \
     --ignore-src -r -y && \
    rm -rf /var/lib/apt/lists/*

RUN source /opt/ros/humble/setup.bash && \
    colcon build --packages-select navi_app

CMD ["bash"]
