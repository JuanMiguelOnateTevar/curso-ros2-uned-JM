#curso-ros2-uned-jm/mini_camera_system/mini_camera_system/viewer_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from rclpy.qos import qos_profile_sensor_data
import numpy as np
import cv2
from cv_bridge import CvBridge

class ViewerNode(Node):
    def __init__(self):
        super().__init__('viewer_node')
        self.bridge = CvBridge()
        self.image_subscription = self.create_subscription(
            msg_type=Image,
            topic='/camera/image_processed',
            callback=self.image_callback,
            qos_profile=qos_profile_sensor_data
        )

    def image_callback(self, msg_img):
        self.get_logger().info(f'Imagen de las {msg_img.header.stamp}')
        
        try: 
            img = self.bridge.imgmsg_to_cv2(msg_img, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Error convirtiendo imagen: {e}')
            return
        
        cv2.namedWindow("cam", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("cam", 640, 480)
        cv2.imshow("cam", img)
        cv2.waitKey(1)

def main(args=None) -> None:
    rclpy.init()
    node = None
    try:
        node = ViewerNode()
        rclpy.spin(node)
    except Exception as e:
        print(f"Se ha producido un error: {e}")
    finally:
        if node is not None:
            node.destroy_node()
            cv2.destroyAllWindows()
        rclpy.shutdown()