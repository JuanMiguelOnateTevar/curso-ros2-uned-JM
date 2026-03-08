#curso-ros2-uned-JM/executor_experiments/executor_experiments/experiment_2_multi_thread.py
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import threading
import time

class ExperimentMultiThread(Node):

    def __init__(self):
        super().__init__("experiment_2_multi_thread")
        self.callback_group = ReentrantCallbackGroup()
        self.timer_a = self.create_timer(1.0, self.callback_a, 
                                callback_group=self.callback_group)
        self.timer_b = self.create_timer(1.0, self.callback_b, 
                                callback_group=self.callback_group)

    def callback_a(self):
        print(f"{threading.get_ident():.2f} A start")
        time.sleep(3)
        print(f"{threading.get_ident():.2f} A end")

    def callback_b(self):
        print(f"{threading.get_ident():.2f} B")

def main(args=None):
    rclpy.init(args=args)
    node = ExperimentMultiThread()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)
    executor.spin()