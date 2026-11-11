import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import time

class TurtleObstacleAvoider(Node):
    def __init__(self):
        super().__init__('turtle_obstacle_avoider')
        self.pose_subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )
        self.is_avoiding = False

    def pose_callback(self, msg):
        obstacle_min_x = 3.0
        obstacle_max_x = 7.0
        obstacle_min_y = 3.0
        obstacle_max_y = 7.0

        map_min_x = 0.5
        map_max_X = 10.5
        map_min_y = 0.5
        map_max_y = 10.5

        if (msg.x <= map_min_x or msg.x >= map_max_X or msg.y <= map_min_y or msg.y >= map_max_y) and not self.is_avoiding:
            self.get_logger().warn("Hit the wall! changing direction.")
            self.avoid_wall()
        elif (obstacle_min_x <= msg.x <= obstacle_max_x) and (obstacle_min_y <= msg.y <= obstacle_max_y) and not self.is_avoiding:
            self.get_logger().warn("Obstacle detected! changing direction")
            self.avoid_wall()
        else :
            twist = Twist()
            twist.linear.x = 1.0
            twist.angular.z = 0.0
            self.cmd_vel_publisher.publish(twist)
            self.is_avoiding = False

    def avoid_wall(self):
        self.is_avoiding = True
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 1.0
        self.cmd_vel_publisher.publish(twist)
        time.sleep(1.0)

        twist.linear.x = 1.0
        twist.angular.z = 0.0
        self.cmd_vel_publisher.publish(twist)
        time.sleep(2.0)

        self.is_avoiding = False


def main(args=None):
    rclpy.init(args=args)
    node=TurtleObstacleAvoider()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()