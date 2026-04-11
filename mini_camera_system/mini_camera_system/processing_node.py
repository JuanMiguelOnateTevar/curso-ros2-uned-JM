#curso-ros2-uned-jm/mini_camera/system/mini_camera_system/processing_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
import cv2
from cv_bridge import CvBridge
import time

class ProcessingNode(Node):
    def __init__(self):
        super().__init__('processing_node')

        qos = QoSProfile(
            depth = 10,
            reliability =  ReliabilityPolicy.BEST_EFFORT,
            durability =DurabilityPolicy.VOLATILE,
            history = HistoryPolicy.KEEP_LAST
        )

        self.bridge = CvBridge()

        self.subscriptor_camera = self.create_subscription(
            msg_type=Image,
            topic='/camera/frame_raw',
            qos_profile=qos,
            callback=self.image_callback
        )

        self.publishers_img_processed = self.create_publisher(
            msg_type=Image,
            topic='/camera/image_processed',
            qos_profile=qos
        )


    def image_callback(self, img_msg):
        self.header_original = img_msg.header.stamp
        self.id_image = img_msg.header.stamp.sec
        self.get_logger().info(f'Nueva imagen {img_msg.header.stamp.sec}')
        try:
            img = self.bridge.imgmsg_to_cv2(img_msg=img_msg, desired_encoding='bgr8')
            self.preprocess_frame(img_cv=img)
        except Exception as e:
            self.get_logger().error(f'Se a producido un error: {e}')
            return
        
    def preprocess_frame(self, img_cv):
        img_cv_recort = img_cv[10:1070, 450:1450]
        img_cv_blur = cv2.medianBlur(img_cv_recort, 5)
        self.get_logger().info(f'Imagen procesada {self.id_image}')
        # cv2.namedWindow('img_cv_blur', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('img_cv_blur', [480, 640])
        # cv2.imshow('img_cv_blur', img_cv_blur)
        # cv2.waitKey(1)
        self.analyze_frame(img_preprocess=img_cv_blur)

    def analyze_frame(self, img_preprocess):
        #Simulacion del retardo de un modelo de IA
        time.sleep(0.2)
        img_analyze = img_preprocess.copy()
        cv2.putText(img=img_analyze, text='NOK', org= [10, 50],
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2, 
                    color=[0, 0, 255], thickness=2)
        # cv2.namedWindow('img_analyze', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('img_analyze', [480, 640])
        # cv2.imshow('img_analyze', img_analyze)
        # cv2.waitKey(1)
        self.get_logger().info(f'Imagen analizada {self.id_image}')
        self.publish_processed_image(img_processed=img_analyze)

    def publish_processed_image(self, img_processed):
        img_processed_msg = self.bridge.cv2_to_imgmsg(img_processed, encoding='bgr8')
        img_processed_msg.header.stamp = self.header_original
        self.publishers_img_processed.publish(img_processed_msg)
        self.get_logger().info(f'Imagen publicada {self.id_image}')

def main(args=None):
    rclpy.init(args=args)
    try:
        node = ProcessingNode()
        rclpy.spin(node)
    except Exception as e:
        print(f'Se ha producido un error: {e}')
    finally:
        if node is not None:
            node.destroy_node()
            #cv2.destroyAllWindows()
        rclpy.shutdown()