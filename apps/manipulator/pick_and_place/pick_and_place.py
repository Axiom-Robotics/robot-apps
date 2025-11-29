#!/usr/bin/env python3
# pick_and_place.py - Basic pick and place routine for UR5

"""
Pick and Place App for UR5 Manipulator
Picks up an object and places it at a different location
Uses pre-defined joint positions for simplicity
"""

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time

class PickAndPlaceNode(Node):
    def __init__(self):
        super().__init__('pick_and_place_node')
        
        # Publisher for joint trajectory commands
        self.joint_pub = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )
        
        # Joint names for UR5
        self.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]
        
        self.get_logger().info('🦾 Pick and Place App Started!')
        self.get_logger().info('📦 Executing pick and place sequence...')
        
        # Wait for publisher to be ready
        time.sleep(1.0)
        
        # Execute the sequence
        self.execute_pick_and_place()
    
    def move_to_position(self, positions, duration_sec=3.0, description="Moving"):
        """Move joints to specified positions"""
        
        self.get_logger().info(f'🎯 {description}...')
        
        # Create trajectory message
        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names
        
        # Create trajectory point
        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start = Duration(sec=int(duration_sec), nanosec=0)
        
        trajectory.points.append(point)
        
        # Publish trajectory
        self.joint_pub.publish(trajectory)
        
        # Wait for movement to complete
        time.sleep(duration_sec + 0.5)
        
        self.get_logger().info(f'✅ {description} complete')
    
    def execute_pick_and_place(self):
        """Execute complete pick and place sequence"""
        
        # === STEP 1: Home Position ===
        self.move_to_position(
            positions=[0.0, -1.57, 1.57, -1.57, -1.57, 0.0],
            duration_sec=3.0,
            description="Moving to home position"
        )
        
        # === STEP 2: Pre-Pick Position (above object) ===
        self.move_to_position(
            positions=[0.5, -1.2, 1.8, -2.2, -1.57, 0.0],
            duration_sec=3.0,
            description="Moving to pre-pick position"
        )
        
        # === STEP 3: Pick Position (lower to object) ===
        self.move_to_position(
            positions=[0.5, -0.8, 1.5, -2.3, -1.57, 0.0],
            duration_sec=2.0,
            description="Lowering to pick object"
        )
        
        self.get_logger().info('🤏 Gripper closing... (simulated)')
        time.sleep(1.0)
        
        # === STEP 4: Lift Object ===
        self.move_to_position(
            positions=[0.5, -1.2, 1.8, -2.2, -1.57, 0.0],
            duration_sec=2.0,
            description="Lifting object"
        )
        
        # === STEP 5: Move to Place Location ===
        self.move_to_position(
            positions=[-0.5, -1.2, 1.8, -2.2, -1.57, 0.0],
            duration_sec=4.0,
            description="Moving to place location"
        )
        
        # === STEP 6: Lower to Place Position ===
        self.move_to_position(
            positions=[-0.5, -0.8, 1.5, -2.3, -1.57, 0.0],
            duration_sec=2.0,
            description="Lowering to place position"
        )
        
        self.get_logger().info('✋ Gripper opening... (simulated)')
        time.sleep(1.0)
        
        # === STEP 7: Retract ===
        self.move_to_position(
            positions=[-0.5, -1.2, 1.8, -2.2, -1.57, 0.0],
            duration_sec=2.0,
            description="Retracting from object"
        )
        
        # === STEP 8: Return Home ===
        self.move_to_position(
            positions=[0.0, -1.57, 1.57, -1.57, -1.57, 0.0],
            duration_sec=3.0,
            description="Returning to home position"
        )
        
        self.get_logger().info('✅ 📦 Pick and Place Complete!')
        self.get_logger().info('🎉 All operations finished successfully')


def main(args=None):
    rclpy.init(args=args)
    node = PickAndPlaceNode()
    
    try:
        # Keep node alive briefly
        time.sleep(2.0)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
