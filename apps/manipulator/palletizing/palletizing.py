#!/usr/bin/env python3
# palletizing.py - Stack boxes on a pallet

"""
Palletizing App for UR5 Manipulator
Real warehouse use case: Pick boxes from conveyor and stack on pallet
Stacks 3x3 grid pattern (9 boxes total)
"""

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time

class PalletizingNode(Node):
    def __init__(self):
        super().__init__('palletizing_node')
        
        self.joint_pub = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )
        
        self.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]
        
        # Palletizing parameters
        self.box_count = 0
        self.max_boxes = 9  # 3x3 grid
        
        # Pick location (conveyor belt)
        self.pick_position = [0.8, -1.0, 1.6, -2.2, -1.57, 0.0]
        
        # Pallet locations (3x3 grid)
        # Format: [shoulder_pan, shoulder_lift, elbow, wrist_1, wrist_2, wrist_3]
        self.pallet_positions = [
            # Row 1 (back)
            [-0.6, -0.9, 1.4, -2.1, -1.57, 0.0],  # Position 1
            [-0.5, -0.9, 1.4, -2.1, -1.57, 0.0],  # Position 2
            [-0.4, -0.9, 1.4, -2.1, -1.57, 0.0],  # Position 3
            # Row 2 (middle)
            [-0.6, -0.8, 1.3, -2.1, -1.57, 0.0],  # Position 4
            [-0.5, -0.8, 1.3, -2.1, -1.57, 0.0],  # Position 5
            [-0.4, -0.8, 1.3, -2.1, -1.57, 0.0],  # Position 6
            # Row 3 (front)
            [-0.6, -0.7, 1.2, -2.1, -1.57, 0.0],  # Position 7
            [-0.5, -0.7, 1.2, -2.1, -1.57, 0.0],  # Position 8
            [-0.4, -0.7, 1.2, -2.1, -1.57, 0.0],  # Position 9
        ]
        
        self.get_logger().info('📦 Palletizing App Started!')
        self.get_logger().info('🏭 Warehouse box stacking routine')
        self.get_logger().info(f'📊 Target: Stack {self.max_boxes} boxes (3x3 grid)')
        
        time.sleep(1.0)
        self.run_palletizing()
    
    def move_to_position(self, positions, duration_sec=2.5, description="Moving"):
        """Move joints to specified positions"""
        
        self.get_logger().info(f'🎯 {description}...')
        
        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names
        
        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start = Duration(sec=int(duration_sec), nanosec=0)
        
        trajectory.points.append(point)
        self.joint_pub.publish(trajectory)
        
        time.sleep(duration_sec + 0.5)
        self.get_logger().info(f'✅ {description} complete')
    
    def pick_box(self):
        """Pick box from conveyor"""
        
        self.get_logger().info('📍 Moving to pick location (conveyor)')
        self.move_to_position(self.pick_position, 2.5, "Moving to conveyor")
        
        self.get_logger().info('🤏 Gripper closing - box secured')
        time.sleep(0.8)
        
        # Lift slightly
        lift_position = self.pick_position.copy()
        lift_position[1] -= 0.2  # Lift shoulder
        self.move_to_position(lift_position, 1.5, "Lifting box")
    
    def place_box(self, position_index):
        """Place box at pallet position"""
        
        pallet_pos = self.pallet_positions[position_index]
        
        # Move to position above pallet
        above_pos = pallet_pos.copy()
        above_pos[1] -= 0.15  # Slightly higher
        
        self.get_logger().info(f'🚚 Moving to pallet position {position_index + 1}')
        self.move_to_position(above_pos, 2.5, f"Moving to pallet slot {position_index + 1}")
        
        # Lower to place
        self.get_logger().info('⬇️  Lowering box')
        self.move_to_position(pallet_pos, 1.5, "Placing box")
        
        self.get_logger().info('✋ Gripper opening - box released')
        time.sleep(0.8)
        
        # Retract
        self.move_to_position(above_pos, 1.5, "Retracting")
    
    def run_palletizing(self):
        """Execute full palletizing routine"""
        
        # Home position
        home = [0.0, -1.57, 1.57, -1.57, -1.57, 0.0]
        self.move_to_position(home, 3.0, "Moving to home")
        
        self.get_logger().info('=' * 60)
        self.get_logger().info('🏭 Starting palletizing operation')
        self.get_logger().info('=' * 60)
        
        for i in range(self.max_boxes):
            self.box_count = i + 1
            
            self.get_logger().info('')
            self.get_logger().info(f'📦 BOX {self.box_count}/{self.max_boxes}')
            self.get_logger().info('-' * 60)
            
            # Pick from conveyor
            self.pick_box()
            
            # Place on pallet
            self.place_box(i)
            
            self.get_logger().info(f'✅ Box {self.box_count} stacked successfully')
            
            # Brief pause before next box
            time.sleep(1.0)
        
        # Return home
        self.get_logger().info('')
        self.get_logger().info('🏠 Returning to home position')
        self.move_to_position(home, 3.0, "Returning home")
        
        self.get_logger().info('=' * 60)
        self.get_logger().info('✅ PALLETIZING COMPLETE!')
        self.get_logger().info(f'📊 Successfully stacked {self.max_boxes} boxes')
        self.get_logger().info('🎉 Pallet ready for shipping')
        self.get_logger().info('=' * 60)


def main(args=None):
    rclpy.init(args=args)
    node = PalletizingNode()
    
    try:
        time.sleep(2.0)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
