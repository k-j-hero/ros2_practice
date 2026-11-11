import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import math
import time

class RRBotController(Node):
    def __init__(self):
        super().__init__('rrbot_controller')
        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/forward_position_controller/commands',
            10
        )

        self.BASE_HEIGHT = 2.0
        self.L1 = 1.0
        self.L2 = 1.0

    def ik_rrbot(self, x, z):
        z_rel = z - self.BASE_HEIGHT
        
        r = math.sqrt(x**2 + z_rel**2)

        if r > self.L1 + self.L2 or r < abs(self.L1 - self.L2):
            print(f"Target position ({x}, {z}) is out of reach")
            return None

        cos_q2 = (r**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        sin_q2 = -math.sqrt(1 - cos_q2**2)
        q2 = math.atan2(sin_q2, cos_q2)

        q1 = math.atan2(x,z_rel) - math.atan2(self.L2 * sin_q2, self.L1 + self.L2 * cos_q2)

        return q1, q2

    def send_joint_command(self, q1, q2):
        msg = Float64MultiArray()
        msg.data = [q1, q2]
        self.publisher.publish(msg)
        print(f"Joint command sent: [q1={q1:.4f}, q2={q2:.4f}]")

def main(args=None):
    rclpy.init(args=args)
    node = RRBotController()

    while True:     
        try:
            cx = float(input("Enter the center x coordinate: "))
            cz = float(input("Enter the center z coordinate: "))            
            r = float(input("Enter the radius: "))

        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue

        steps = 25
        prev_q1 = None
        prev_q2 = None
        for i in range(steps*500+1):
            theta = (2 * math.pi / steps) * i

            target_x = cx + r * math.cos(theta)
            target_z = cz + (r / 2.0) * math.sin(2 * theta)

            ik_result = node.ik_rrbot(target_x, target_z)
            if ik_result:
                q1, q2 = ik_result

                if prev_q1 is not None:
                    diff_q1 = prev_q1 - q1
                    q1 += 2 * math.pi * round(diff_q1 / (2 * math.pi))
                    
                    diff_q2 = prev_q2 - q2
                    q2 += 2 * math.pi * round(diff_q2 / (2 * math.pi))

                prev_q1 = q1
                prev_q2 = q2
                
                print(f"Input: (x center = {cx:.4f}, z center = {cz:.4f})")
                print(f"Joint angles (radians): [q1={q1:.4f}, q2={q2:.4f}]")
                print(f"Joint angles (degrees): [q1={math.degrees(q1):.4f}, q2={math.degrees(q2):.4f}]")

                node.send_joint_command(q1, q2)
                
                rclpy.spin_once(node, timeout_sec=0.3)

            
            else:
                print("Unable to calculate inverse kinematics for the given coordinate")
                break
        choice = input("Do you want to enter another coordinate? (y/n)")
        if choice.lower() != 'y':
            break
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

