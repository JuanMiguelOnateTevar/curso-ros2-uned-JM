import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
import asyncio
from comuni_interfaces.srv import Operacion
from comuni_interfaces.action import Operacion1
from rclpy.executors import MultiThreadedExecutor

class NodeC(Node):

    def __init__(self):
        super().__init__('Node_C')
        self.action = ActionServer(
            self,
            Operacion1,
            'operacion1',
            self.execute_callback
        )
        self.client = self.create_client(Operacion, 'operacion')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.request = Operacion.Request()
    
    def execute_callback(self, goal_handle):
        numero = goal_handle.request.numero
        iteraciones = goal_handle.request.iteraciones
        for i in range(iteraciones):
            numero = self.llamar_servicio_B(numero)

            feedback_msg = Operacion1.Feedback()
            self.get_logger().info(f'Iteracion {i}')
            feedback_msg.iteraciones_restantes = iteraciones-i-1
            feedback_msg.resultado_parcial = numero
            goal_handle.publish_feedback(feedback_msg)


        result = Operacion1.Result()
        result.resultado = numero
        goal_handle.succeed()

        return result

    def llamar_servicio_B(self, numero):
        self.request.numero = numero
        self.future = self.client.call_async(self.request)
        # while not self.future.done():
        #     rclpy.spin_once(self, timeout_sec=0.05)
        return self.future.result().resultado


def main(args=None):
    rclpy.init(args=args)
    node = NodeC()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    node.destroy_node()
    rclpy.shutdown()