import rclpy
from rclpy.node import Node
from comuni_interfaces.srv import Operacion

class NodeB(Node):

    def __init__(self):
        super().__init__('node_B')
        self.srv = self.create_service(
            Operacion,
            'operacion',
            self.callback_operacion
        )       


    def callback_operacion(self, request, response):
        response.resultado = request.numero * 2
        return response

def main(args=None):
    rclpy.init(args=args)
    node = NodeB()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()






