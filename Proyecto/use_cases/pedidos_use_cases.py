from domain.entities import Pedido
from domain.repository_interfaces import PedidoRepository
import uuid

class CrearPedidoUseCase:
    def __init__(self, pedido_repo: PedidoRepository):
        self.pedido_repo = pedido_repo
        
    def execute(self, id_cliente: str, direccion: str, platos_ids: list, hora_creacion) -> str:
        # En una app real aquí se calcularía el importe leyendo los platos
        nuevo_id = str(uuid.uuid4())
        pedido = Pedido(
            id_pedido=nuevo_id,
            id_cliente=id_cliente,
            direccion_entrega=direccion,
            hora_entrega_aprox=hora_creacion,
            estado='Recibido',
            importe_total=0.0, # Placeholder
            platos_ids=platos_ids
        )
        self.pedido_repo.guardar(pedido)
        return nuevo_id

class ActualizarEstadoPedidoUseCase:
    def __init__(self, pedido_repo: PedidoRepository):
        self.pedido_repo = pedido_repo

    def execute(self, id_pedido: str, nuevo_estado: str, id_empleado: str):
        self.pedido_repo.actualizar_estado(id_pedido, nuevo_estado, id_empleado)
