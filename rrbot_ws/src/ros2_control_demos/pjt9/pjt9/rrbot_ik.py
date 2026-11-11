import math

class RRBotController:
    def __init__(self):
        self.BASE_HEIGHT = 2.0 # 베이스의 높이
        self.L1 = 1.0 # 첫 번째 링크의 길이
        self.L2 = 1.0 # 두 번째 링크의 길이

    def ik_rrbot(self, x, z):
        # x: 엔드 이펙터의 수평 위치 (베이스 중앙으로부터의 거리, 오른쪽이 양수)

        # z: 엔드 이펙터의 수직 위치 (베이스 중앙으로부터의 높이, 위쪽이 양수)

        # 전체 길이 계산
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

def main():
    controller = RRBotController()
    print("RRBot Inverse Kinematics Calculator")
    print("Enter 'q' to quit")

    while True:
        try:
            x_input = input("Enter x coordinate (horizontal, 0 is at base center, right is positive): ")
            if x_input.lower() == 'q':
                break
            x = float(x_input)            
            
            z_input = input("Enter z coordinate (vertical, 0 is at base center, up is positive): ")
            if z_input.lower() == 'q':
                break
            z = float(z_input)

            ik_result = controller.ik_rrbot(x, z)

            if ik_result:
                q1, q2 = ik_result
                print(f"Input coordinates: (x={x:.4f}, z={z:.4f})")
                print(f"Joint angles (radians): [q1={q1:.4f}, q2={q2:.4f}]")
                print(f"Joint angles (degrees): [q1={math.degrees(q1):.4f}, q2={math.degrees(q2):.4f}]")
            else:
                print("Unable to calculate inverse kinematics for the given coordinates.")
            
            print()  # Empty line for better readability
        except ValueError:
            print("Invalid input. Please enter numeric values.")

    print("Calculator closed.")

if __name__ == "__main__":
    main()
