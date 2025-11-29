#!/usr/bin/env python3
# follow_me.py - LiDAR-based Follow-Me app for TurtleBot3

"""
Follow-Me App using LiDAR
Tracks the closest object and follows it at a safe distance
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

class FollowMeNode(Node):
    def __init__(self):
        super().__init__('follow_me_node')
        
        # Subscribe to LiDAR
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        
        # Publish velocity commands
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Parameters
        self.safe_distance = 0.6  # meters
        self.max_speed = 0.2      # m/s
        self.angular_gain = 1.5
        
        self.get_logger().info('🎯 Follow-Me activated!')
        self.get_logger().info(f'📏 Safe distance: {self.safe_distance}m')
    
    def scan_callback(self, msg):
        """Process LiDAR scan and follow closest object"""
        
        ranges = np.array(msg.ranges)
        ranges = np.where(np.isinf(ranges), 10.0, ranges)
        
        min_idx = np.argmin(ranges)
        min_dist = ranges[min_idx]
        angle = msg.angle_min + min_idx * msg.angle_increment
        
        cmd = Twist()
        
        # Distance control
        if min_dist > self.safe_distance + 0.1:
            cmd.linear.x = min(self.max_speed, (min_dist - self.safe_distance) * 0.2)
            self.get_logger().info(f'⬆️ Following: {min_dist:.2f}m', throttle_duration_sec=1.0)
        elif min_dist < self.safe_distance - 0.1:
            cmd.linear.x = -0.1
            self.get_logger().info(f'⬇️ Too close: {min_dist:.2f}m', throttle_duration_sec=1.0)
        else:
            cmd.linear.x = 0.0
            self.get_logger().info(f'✅ Perfect: {min_dist:.2f}m', throttle_duration_sec=1.0)
        
        # Steering
        cmd.angular.z = -angle * self.angular_gain
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = FollowMeNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
