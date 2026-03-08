import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PublisherNode(Node):

    def __init__(self):
        super().__init__('publisher_node')

        self.publisher_ = self.create_publisher(String, 'chatter', 10)

        self.timer = self.create_timer(1.0, self.publish_message)

        self.counter = 0

    def publish_message(self):
        msg = String()
        msg.data = f"Mensaje numero {self.counter}"
        self.publisher_.publish(msg)
        self.get_logger().info(f"Publicado: {msg.data}")
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

