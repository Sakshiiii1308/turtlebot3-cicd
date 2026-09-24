pipeline {
    agent {
        label 'ros2'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Sakshiiii1308/turtlebot3-cicd.git'
            }
        }

        stage('ROS 2 Build') {
            steps {
                sh '''
                    set -e

                    docker exec ros2-humble \
                        rm -rf /tmp/jenkins-ros2

                    docker exec ros2-humble \
                        mkdir -p /tmp/jenkins-ros2

                    docker cp ros2_ws/src \
                        ros2-humble:/tmp/jenkins-ros2/

                    docker exec ros2-humble bash -c '
                        set -e
                        source /opt/ros/humble/setup.bash
                        cd /tmp/jenkins-ros2
                        colcon build --packages-select navi_app
                    '
                '''
            }
        }

        stage('ROS 2 Tests') {
            steps {
                sh '''
                    set -e

                    docker exec ros2-humble bash -c '
                        set -e
                        source /opt/ros/humble/setup.bash
                        cd /tmp/jenkins-ros2

                        colcon test --packages-select navi_app \
                            --pytest-args -k "not navigation_integration"

                        colcon test-result --verbose
                    '
                '''
            }
        }
        stage('ROS 2 Tests') {
            steps {
                sh '''
                    docker exec ros2-humble bash -lc '
                        source /opt/ros/humble/setup.bash
                        source /tmp/jenkins-ros2/install/setup.bash
                        cd /tmp/jenkins-ros2

                        colcon test --packages-select navi_app \
                            --pytest-args -k "not navigation_integra>

                        colcon test-result --verbose
                    '
                '''
            }
        }

        stage('Check Nav2 Connection'){
            steps {
                sh '''
                    docker exec ros2-humble bash -lc '
                        source /opt/ros/humble/setup.bash
                        ros2 action list | grep -Fx /navigate_to_pose
                    '
                '''
           }
        }  
    }
}
