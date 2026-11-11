import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
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
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        self.BASE_HEIGHT = 2.0  # 베이스의 높이
        self.L1 = 1.0  # 첫 번째 링크의 길이
        self.L2 = 1.0  # 두 번째 링크의 길이
        self.current_joint_positions = [0.0, 0.0]
        self.tolerance = 0.06  # 라디안 단위의 허용 오차

    def ik_rrbot(self, x, z):
        r = math.sqrt(x**2 + z**2)
        if r > self.L1 + self.L2 or r < abs(self.L1 - self.L2):
            print(f"Target position ({x}, {z}) is out of reach")
            return None
        cos_q2 = (r**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        sin_q2 = -math.sqrt(1 - cos_q2**2)
        q2 = math.atan2(sin_q2, cos_q2)
        q1 = math.atan2(x, z) - math.atan2(self.L2 * sin_q2, self.L1 + self.L2 * cos_q2)
        return q1, q2

    def send_joint_command(self, q1, q2):
        msg = Float64MultiArray()
        msg.data = [q1, q2]
        self.publisher.publish(msg)
        print(f"Joint command sent: [q1={q1:.4f}, q2={q2:.4f}]")

    def joint_state_callback(self, msg):
        self.current_joint_positions = msg.position[:2]  # 첫 두 관절 사용

    def wait_for_position(self, target_q1, target_q2, timeout=5.0):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if (abs(self.current_joint_positions[0] - target_q1) <= self.tolerance and
                abs(self.current_joint_positions[1] - target_q2) <= self.tolerance):
                return True
            rclpy.spin_once(self, timeout_sec=0.1)
        print("Timeout: Target position not reached within the specified time.")
        return False

    def smooth_joint_transition(self, prev_q, next_q):
        diff = next_q - prev_q
        if abs(diff) > math.pi:
            if diff > 0:
                next_q -= 2 * math.pi
            else:
                next_q += 2 * math.pi
        return next_q

    def draw_figure_eight(self, diameter):
        points = []
        for t in range(0, 360, 5):  # 5도 간격으로 계산
            angle = math.radians(t)
            x = diameter * math.sin(angle)
            z = diameter * math.sin(angle) * math.cos(angle)
            points.append((x, z))
        
        prev_q1, prev_q2 = None, None
        for x, z in points:
            ik_result = self.ik_rrbot(x, z)
            if ik_result:
                q1, q2 = ik_result
                if prev_q1 is not None and prev_q2 is not None:
                    q1 = self.smooth_joint_transition(prev_q1, q1)
                    q2 = self.smooth_joint_transition(prev_q2, q2)
                self.send_joint_command(q1, q2)
                if not self.wait_for_position(q1, q2):
                    print(f"Failed to reach position ({x:.4f}, {z:.4f})")
                    return False  # 실패 시 즉시 종료
                prev_q1, prev_q2 = q1, q2
            else:
                print(f"Point ({x:.4f}, {z:.4f}) is out of reach")
                return False  # 실패 시 즉시 종료
        return True  # 모든 점을 성공적으로 통과

def main(args=None):
    rclpy.init(args=args)
    node = RRBotController()

    while True:
        try:
            diameter = float(input("Enter the diameter for the figure-eight (or 0 to quit): "))
            if diameter == 0:
                break
            if node.draw_figure_eight(diameter):
                print("Figure-eight completed successfully.")
            else:
                print("Failed to complete figure-eight. Please try again with different parameters.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()