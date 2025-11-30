#!/usr/bin/env python3
# quality_scan.py - Inspect object from multiple angles

"""
Quality Inspection App for UR5 Manipulator
Real manufacturing use case: Inspect product from 6 angles
Simulates camera-based quality control inspection
"""

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time

class QualityScanNode(Node):
    def __init__(self):
        super().__init__('quality_scan_node')
        
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
        
        # Inspection angles (camera views around object)
        self.inspection_positions = {
            'front': [0.0, -1.2, 1.8, -2.2, -1.57, 0.0],
            'right': [0.8, -1.2, 1.8, -2.2, -1.57, 0.0],
            'back': [1.57, -1.2, 1.8, -2.2, -1.57, 0.0],
            'left': [-0.8, -1.2, 1.8, -2.2, -1.57, 0.0],
            'top': [0.0, -1.8, 2.2, -2.0, -1.57, 0.0],
            'bottom': [0.0, -0.6, 1.2, -2.2, -1.57, 0.0]
        }
        
        # Defect detection results (simulated)
        self.inspection_results = {}
        
        self.get_logger().info('🔍 Quality Inspection App Started!')
        self.get_logger().info('🏭 Manufacturing quality control scan')
        self.get_logger().info('📷 6-angle camera inspection system')
        
        time.sleep(1.0)
        self.run_inspection()
    
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
    
    def capture_image(self, angle_name):
        """Simulate camera capture and analysis"""
        
        self.get_logger().info(f'📸 Capturing image from {angle_name} angle...')
        time.sleep(1.0)  # Simulate image processing
        
        # Simulate defect detection (random result)
        import random
        has_defect = random.random() < 0.1  # 10% defect rate
        
        if has_defect:
            self.get_logger().warn(f'⚠️  Potential defect detected at {angle_name} angle!')
            result = 'DEFECT FOUND'
        else:
            self.get_logger().info(f'✅ {angle_name.capitalize()} angle: PASS')
            result = 'PASS'
        
        self.inspection_results[angle_name] = result
        return result
    
    def run_inspection(self):
        """Execute full quality inspection routine"""
        
        # Home position
        home = [0.0, -1.57, 1.57, -1.57, -1.57, 0.0]
        self.move_to_position(home, 3.0, "Moving to home")
        
        self.get_logger().info('=' * 70)
        self.get_logger().info('🔬 Starting Quality Inspection')
        self.get_logger().info('=' * 70)
        
        inspection_sequence = ['front', 'right', 'back', 'left', 'top', 'bottom']
        
        for i, angle in enumerate(inspection_sequence, 1):
            self.get_logger().info('')
            self.get_logger().info(f'📷 INSPECTION {i}/6: {angle.upper()} VIEW')
            self.get_logger().info('-' * 70)
            
            # Move to inspection position
            position = self.inspection_positions[angle]
            self.move_to_position(
                position, 
                2.5, 
                f"Moving camera to {angle} angle"
            )
            
            # Capture and analyze
            self.capture_image(angle)
            
            # Pause for stability
            time.sleep(0.5)
        
        # Return home
        self.get_logger().info('')
        self.get_logger().info('🏠 Returning to home position')
        self.move_to_position(home, 3.0, "Returning home")
        
        # Generate inspection report
        self.generate_report()
    
    def generate_report(self):
        """Generate final inspection report"""
        
        self.get_logger().info('')
        self.get_logger().info('=' * 70)
        self.get_logger().info('📊 QUALITY INSPECTION REPORT')
        self.get_logger().info('=' * 70)
        
        defects_found = sum(1 for result in self.inspection_results.values() if result == 'DEFECT FOUND')
        total_checks = len(self.inspection_results)
        
        self.get_logger().info(f'Total angles inspected: {total_checks}')
        self.get_logger().info(f'Angles passed: {total_checks - defects_found}')
        self.get_logger().info(f'Defects detected: {defects_found}')
        self.get_logger().info('')
        
        # Detailed results
        for angle, result in self.inspection_results.items():
            status = '✅ PASS' if result == 'PASS' else '❌ FAIL'
            self.get_logger().info(f'{angle.capitalize():10} angle: {status}')
        
        self.get_logger().info('')
        
        # Final verdict
        if defects_found == 0:
            self.get_logger().info('🎉 VERDICT: PRODUCT APPROVED FOR SHIPPING')
            self.get_logger().info('✅ All quality checks passed')
        else:
            self.get_logger().warn('⚠️  VERDICT: PRODUCT REJECTED')
            self.get_logger().warn(f'❌ Failed {defects_found} quality check(s)')
            self.get_logger().info('📋 Product marked for rework or disposal')
        
        self.get_logger().info('=' * 70)


def main(args=None):
    rclpy.init(args=args)
    node = QualityScanNode()
    
    try:
        time.sleep(2.0)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

