import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker

class ObstacleMarkerPublisher(Node):
    def __init__(self):
        super().__init__('obstacle_marker_publisher')
        self.publisher_ = self.create_publisher(Marker, 'visualization_marker', 10)
        self.timer = self.create_timer(0.5, self.publish_marker)

    def publish_marker(self):
        marker = Marker()
        marker.header.frame_id = "world"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "obstacle"
        marker.id = 0
        marker.type = Marker.CUBE
        marker.action = Marker.ADD

        marker.pose.position.x = 4.0
        marker.pose.position.y = 4.0
        marker.pose.position.z = 0.0

        marker.scale.x = 4.0
        marker.scale.y = 4.0
        marker.scale.z = 1.0

        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        self.publisher_.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleMarkerPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
