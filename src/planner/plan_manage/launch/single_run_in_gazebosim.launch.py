import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import PythonExpression
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():
    # 定义参数的 LaunchConfiguration
    obj_num = LaunchConfiguration('obj_num', default=10)
    drone_id = LaunchConfiguration('drone_id', default=0)
    
    map_size_x = LaunchConfiguration('map_size_x', default = 50.0)
    map_size_y = LaunchConfiguration('map_size_y', default = 25.0)
    map_size_z = LaunchConfiguration('map_size_z', default = 10.0)
    odom_topic = LaunchConfiguration('odom_topic', default = 'visual_slam/odom')
    
    # Include advanced parameters
    advanced_param_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('ego_planner'), 'launch', 'advanced_param.launch.py')),
        launch_arguments={
            'drone_id': drone_id,
            'map_size_x_': map_size_x,
            'map_size_y_': map_size_y,
            'map_size_z_': map_size_z,
            'odometry_topic': odom_topic,
            'obj_num_set': obj_num,
            
            'camera_pose_topic': 'pcl_render_node/camera_pose',
            'depth_topic': 'pcl_render_node/depth1',
            'cloud_topic': 'pcl_render_node/depth/points',
            
            'cx': str(320.0),
            'cy': str(240.0),
            'fx': str(432.496042035043),
            'fy': str(432.496042035043),
            'max_vel': str(1.0),
            'max_acc': str(2.0),
            'planning_horizon': str(7.5),
            'use_distinctive_trajs': 'True',
            'flight_type': str(2),
            'point_num': str(4),
            'point0_x': str(0.0),
            'point0_y': str(0.0),
            'point0_z': str(3.0),
            
            'point1_x': str(0.0),
            'point1_y': str(0.0),
            'point1_z': str(3.0),
            
            'point2_x': str(0.0),
            'point2_y': str(20.0),
            'point2_z': str(3.0),
            
            'point3_x': str(0.0),
            'point3_y': str(0.0),
            'point3_z': str(3.0),
            
            'point4_x': str(0.0),
            'point4_y': str(20.0),
            'point4_z': str(3.0),

        }.items()
    )
    
    # Trajectory server node
    traj_server_node = Node(
        package='ego_planner',
        executable='traj_server',
        name=['drone_', drone_id, '_traj_server'],
        output='screen',
        remappings=[
            ('position_cmd', ['drone_', drone_id, '_planning/pos_cmd']),
            ('planning/bspline', ['drone_', drone_id, '_planning/bspline'])
        ],
        parameters=[
            {'traj_server/time_forward': 1.0}
        ]
    )

    
    ld = LaunchDescription()
        
    ld.add_action(advanced_param_include)
    ld.add_action(traj_server_node)

    return ld