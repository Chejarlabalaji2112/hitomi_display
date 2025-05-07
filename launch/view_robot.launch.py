from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
import xacro
def generate_launch_description():
    robot_description_content = xacro.process_file('/home/badri/ros2_ws/src/hitomi/urdf/combined.urdf.xacro').toxml() #Command(['xacro ', '/home/badri/ros2_ws/src/hitomi/urdf/combined.urdf.xacro'])
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description_content}],
            output="screen"
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
        ),
    ])

