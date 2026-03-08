#curso-ros2-uned-JM/executor_experiments/executor_experiments/experiment_1_single_thread.py
import rclpy
from rclpy.node import Node
import time

class ExperimentSingleThread(Node):

    def __init__(self):
        super().__init__('experiment_1_single_thread')
        self.timer_a = self.create_timer(1.0, self.callback_a)
        self.timer_b = self.create_timer(1.0, self.callback_b)

    def callback_a(self):
        print(f"{time.time():.2f} A start")
        time.sleep(3)
        print('A end')

    def callback_b(self):
        print(f"{time.time():.2f} B")

def main(args=None):
    rclpy.init(args=args)
    node = ExperimentSingleThread()
    rclpy.spin(node)
