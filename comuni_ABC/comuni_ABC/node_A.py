import sys
import rclpy
from rclpy.node import Node
from comuni_interfaces.srv import Operacion
from rclpy.action import ActionClient
from comuni_interfaces.action import Operacion1

class NodeA(Node):

    def __init__(self):
        super().__init__('Node_A')
        # self.client = self.create_client(Operacion, 'operacion')
        # while not self.client.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('service not available, waiting again...')
        #self.request = Operacion.Request()
        self._action_client = ActionClient(
            self,
            Operacion1,
            'operacion1'
        )
    def send_goal(self, numero, iteraciones):
        self._action_client.wait_for_server()

        goal_msg = Operacion1.Goal()
        goal_msg.numero = numero
        goal_msg.iteraciones = iteraciones

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )   

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'El numero de iteraciones restantes es {feedback.iteraciones_restantes}')
        self.get_logger().info(f'El resultado parcial es {feedback.resultado_parcial}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'El resultado final es {result.resultado}')
        self.destroy_node()
        rclpy.shutdown()

    def entrada(self, numero):
        self.request.numero = numero
        self.future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)
    node = NodeA()
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    responde = node.send_goal(a, b)
    rclpy.spin(node)
    #responde = node.entrada(a)
    #node.get_logger().info(f'Resultado de {a} = {responde.resultado}')
    # node.destroy_node()
    # rclpy.shutdown()