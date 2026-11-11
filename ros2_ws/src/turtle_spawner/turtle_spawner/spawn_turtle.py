import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn

class TurtleSpawner(Node):
    def __init__(self):
        super().__init__('turtle_spawner')
        self.pub1 = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.pub2 = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.request = Spawn.Request()
        self.spawn_new_turtle()
        self.timer = self.create_timer(0.1, self.timer_callback)

    def spawn_new_turtle(self):
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('서비스 연결 대기 중...')

        self.request.x = 5.0
        self.request.y = 5.0
        self.request.theta = 0.0
        self.request.name = 'turtle2'

        self.spawn_client.call_async(self.request)
        self.get_logger().info('turtle2 생성 요청  완료!')

    def timer_callback(self):
        self.velocity = Twist()

        self.velocity.linear.x=2.0
        self.velocity.angular.z=1.0
        self.pub1.publish(self.velocity)

        self.velocity.linear.x = 1.5
        self.velocity.angular.z = -1.0
        self.pub2.publish(self.velocity)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()