from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            namespace='turtlesim1',
            output='screen'
        ),
        Node(
            package='myrobotpackage',
            executable='move_turtle',
            name='square_node',
            namespace='turtlesim1',
            output='screen',
            remappings=[
                ('turtle1/cmd_vel', '/turtlesim1/turtle1/cmd_vel'),
                ('/turtle1/cmd_vel', '/turtlesim1/turtle1/cmd_vel'),
            ],
        ),
    ])
