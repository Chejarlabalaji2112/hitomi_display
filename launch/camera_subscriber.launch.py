from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hitomi',
            executable='camera_subscriber',
            name='camera_subscriber',
            output='screen'
        ),
    ])
