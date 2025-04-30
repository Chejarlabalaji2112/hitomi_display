from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    pkg_name = 'hitomi'
    robot_urdf = os.path.join(FindPackageShare(pkg_name).find(pkg_name), 'urdf', 'total_body.urdf')
    
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': open(robot_urdf).read()}]
        ),
       ExecuteProcess(
            cmd=[
                'ros2', 'run', 'ros_gz_sim', 'create',
                '-name', 'my_robot',
                '-x', '0', '-y', '0', '-z', '0.2',
                '-topic', 'robot_description'
            ],
            output='screen'
        ),
    ])

