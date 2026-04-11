#curso-ros2-uned-jm/mini_camera_system/mini_camera_system/camara_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from rclpy.qos import qos_profile_sensor_data
from cv_bridge import CvBridge
import time

class CameraNode(Node):
    def __init__(self) -> None:
        super().__init__('camara_node')
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.get_logger().error('No se pudo inicializar la camara')
            raise RuntimeError('No se pudo inicializar la camara')
        self.image_publisher = self.create_publisher(
            msg_type=Image,
            topic='/camera/frame_raw',
            qos_profile=qos_profile_sensor_data
        )
        self.publish_timer = self.create_timer(
            timer_period_sec=0.5,
            callback=self.capture_and_publish_image
        )

    def capture_and_publish_image(self):
        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().warning('No se pudo inicializar la camara')
            return
        time_frame = time.asctime()
        cv2.putText(img=frame, text=str(time_frame), org=(20, 40), 
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=(0, 0, 255), thickness=2)
        msg_img = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        msg_img.header.stamp = self.get_clock().now().to_msg()
        msg_img.header.frame_id = "webcam_optical_frame"

        self.get_logger().info('La camara a tomado una imagen con')
        self.publish_image(msg_img)

    def publish_image(self, msg_img):
        self.image_publisher.publish(msg_img)
        self.get_logger().info(
                        f'Imagen publicada: {msg_img.width}x{msg_img.height}, '
                        f'stamp={msg_img.header.stamp}')
        
    def destroy_node(self):
        # Tu limpieza personalizada
        if self.cap.isOpened():
            self.cap.release()
            self.get_logger().info("Cámara liberada correctamente")

        # Llamar al destructor original
        super().destroy_node()
        
def main(args=None) -> None:
    rclpy.init(args=args)
    node = None
    try:
        node = CameraNode()
        rclpy.spin(node)
    except RuntimeError as exc:
        print(f'Error al arrancar el nodo: {exc}')
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()
        



