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

        stage('Docker Hub Push') {
            steps {
               withCredentials([
                   usernamePassword(
                       credentialsId: 'dockerhub-credentials',
                       usernameVariable: 'DOCKER_USER',
                       passwordVariable: 'DOCKER_TOKEN'
                   )
               ]) {
                   sh '''
                       set -e

                       echo "$DOCKER_TOKEN" | docker login \
                           --username "$DOCKER_USER" \
                           --password-stdin

                       docker tag turtlebot3-navigation:latest \
                           "$DOCKER_USER/turtlebot3-navigation:latest"

                       docker push \
                           "$DOCKER_USER/turtlebot3-navigation-latest"

                       docker logout
                   '''
               }
            }
        }
        stage('ROS 2 Tests') {
            steps {
                sh '''
                    set -e

                    docker exec ros2-humble bash -c '
                        set -e
                        cd /tmp/jenkins-ros2

                        source /opt/ros/humble/setup.bash

                        export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
                        export ROS_DOMAIN_ID=0

                        source install/setup.bash

                        colcon test --packages-select navi_app \
                            --pytest-args -k "not TestNavigationIntegration"

                        colcon test-result --verbose
                    '
                '''
            }
        }
        stage('ROS2 Integration Tests') {
            steps {
                sh '''
                    docker exec ros2-humble bash -lc '
                        set -e

                        cd /tmp/jenkins-ros2

                        source /opt/ros/humble/setup.bash                        
                        export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

                        export ROS_DOMAIN_ID=0
                        source install/setup.bash

                        echo "Checking Nav2 lifecycle states"

                        ros2 lifecycle get /bt_navigator
                        ros2 lifecycle get /behavior_server

                        echo "Running integration tests"

                        colcon test --packages-select navi_app \
                            --pytest-args -k "TestNavigationIntegration"

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

        stage('Docker Build') {
           steps {
               sh '''
                  set -e

                    docker build \
                        -t turtlebot3-navigation:latest \
                        -f Dockerfile .
                 '''
            }
         }
    }
}
