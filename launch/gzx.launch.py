import os
import xacro
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    robot_name = "test_bot"
    package_name = "hitomi"

    world_arg = DeclareLaunchArgument(
        'world',
        default_value='empty.sdf',
        description='Specify the world file for Gazebo (eg., empty.sdf)'
    )

    x_arg = DeclareLaunchArgument(
        'x', default_value='0.0', description='Initial X position'
    )

    y_arg = DeclareLaunchArgument(
        'y', default_value='0.0', description='Initial Y position'
        )

    z_arg = DeclareLaunchArgument(
        'z', default_value='0.5', description='Initial Z position'
        )

    roll_arg = DeclareLaunchArgument(
        'R', default_value='0.0', description='Initial Roll'
        )

    pitch_arg = DeclareLaunchArgument(
        'P', default_value='0.0', description='Initial Pitch'
        )

    yaw_arg = DeclareLaunchArgument(
        'Y', default_value='0.0', description='Initial Yaw'
        )   
    
    world_file = LaunchConfiguration('world')
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    roll = LaunchConfiguration('R')
    pitch = LaunchConfiguration('P')
    yaw = LaunchConfiguration('Y')

    robot_model_path = os.path.join(
        get_package_share_directory(package_name),
        'urdf',
        'body.xacro'
    )

    gz_bridge_param_path = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'gz_bridge.yaml')

    robot_description = xacro.process_file(robot_model_path).toxml()

    gazebo_pkg_launch = PythonLaunchDescriptionSource(
        os.path.join(
            get_package_share_directory('ros_gz_sim'),
            'launch',
            'gz_sim.launch.py'
        )
    )

    gazebo_launch = IncludeLaunchDescription(
        gazebo_pkg_launch,
        launch_arguments={
            'gz_args': [f'-r -v 4 ', world_file],
            'on_exit_shutdown': 'true'
        }.items()
    )

    spawn_model_gazebo_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments= [
            '-name', robot_name,
            '-string', robot_description,
            '-x', x,
            '-y', y,
            '-z', z,
            '-R', roll,
            '-P', pitch,
            '-Y', yaw,
            '-allow_renaming', 'false'
        ],
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': robot_description, 'use_sim_time': True}
        ],
        output = 'screen'
    )

    gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={gz_bridge_param_path}'
        ],
        output = 'screen'
    )

    return LaunchDescription(
        [
            world_arg,
            gazebo_launch,
            x_arg,
            y_arg,
            z_arg,
            roll_arg,
            pitch_arg,
            yaw_arg,
            spawn_model_gazebo_node,
            robot_state_publisher_node,
            gz_bridge_node
        ]
    )