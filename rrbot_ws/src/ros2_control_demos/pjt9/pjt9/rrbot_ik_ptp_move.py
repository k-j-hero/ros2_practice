import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray #토픽에 들어갈 데이터 타입 (float로 된 배열)
import math

class RRBotController(Node):
    def __init__(self):
        super().__init__('rrbot_controller')
        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/forward_position_controller/commands',
            10
        )

        self.BASE_HEIGHT = 2.0 # 베이스의 높이
        self.L1 = 1.0 # 첫 번째 링크의 길이
        self.L2 = 1.0 # 두 번째 링크의 길이
        

    def ik_rrbot(self, x, z):
        r = math.sqrt(x**2 + z**2)

        if r > self.L1 + self.L2 or r < abs(self.L1 - self.L2):
            print(f"Target position ({x}, {z}) is out of reach")
            return None
        
        # 두 번째 관절 각도 계산
        cos_q2 = (r**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        sin_q2 = -math.sqrt(1 - cos_q2**2) # elbow down
        q2 = math.atan2(sin_q2, cos_q2)

        # 첫 번째 관절 각도 계산
        q1 = math.atan2(x, z) - math.atan2(self.L2 * sin_q2, self.L1 + self.L2 * cos_q2)

        return q1, q2

    def send_joint_command(self, q1, q2):
        # Mission 
        msg = Float64MultiArray()
        msg.data = [q1, q2]
        self.publisher.publish(msg)
        print(f"Joint command sent: [q1={q1:.4f}, q2={q2:.4f}]")

def main(args=None):
    rclpy.init(args=args)
    node = RRBotController()

    while True:
        try:
            x = float(input("Enter x coordinate (horizontal, 0 is at base center, right is positive): "))
            z = float(input("Enter z coordinate (vertical, 0 is at base center, up is positive): "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue

        ik_result = node.ik_rrbot(x, z)
        if ik_result:
            q1, q2 = ik_result
            print(f"Input coordinates: (x={x:.4f}, z={z:.4f})")
            print(f"Joint angles (radians): [q1={q1:.4f}, q2={q2:.4f}]")
            print(f"Joint angles (degrees): [q1={math.degrees(q1):.4f}, q2={math.degrees(q2):.4f}]")
            node.send_joint_command(q1, q2)
        else:
            print("Unable to calculate inverse kinematics for the given coordinates.")
        choice = input("Do you want to enter another coordinate? (y/n)")
        if choice.lower() != 'y':
            break
        

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
