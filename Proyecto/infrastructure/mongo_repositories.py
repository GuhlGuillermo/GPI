from domain.entities import Pedido, Plato, Menu_Diario
from domain.repository_interfaces import PedidoRepository, CatalogoRepository
from infrastructure.mongo_connection import get_db

class MongoPedidoRepository(PedidoRepository):
    def __init__(self):
        self.collection = get_db()['pedidos']

    def guardar(self, pedido: Pedido) -> None:
        # Convertir dataclass a dict para MongoDB
        data = pedido.__dict__.copy()
        self.collection.update_one(
            {'id_pedido': pedido.id_pedido},
            {'$set': data},
            upsert=True
        )

    def obtener_por_id(self, id_pedido: str):
        data = self.collection.find_one({'id_pedido': id_pedido})
        if data:
            data.pop('_id', None)
            return Pedido(**data)
        return None

    def listar_todos(self):
        return [Pedido(**{k: v for k, v in p.items() if k != '_id'}) for p in self.collection.find()]

    def actualizar_estado(self, id_pedido: str, nuevo_estado: str, id_empleado: str) -> None:
        self.collection.update_one(
            {'id_pedido': id_pedido},
            {'$set': {'estado': nuevo_estado, 'id_empleado': id_empleado}}
        )

class MongoCatalogoRepository(CatalogoRepository):
    def __init__(self):
        self.collection = get_db()['platos']

    def listar_platos_en_carta(self):
        cursor = self.collection.find({'esta_en_carta': True})
        # Si la bd está vacía retornamos algunos hardcoded mockeados por ahora
        platos_db = [Plato(**{k: v for k, v in p.items() if k != '_id'}) for p in cursor]
        if not platos_db:
            return [
                Plato(id_plato="mock1", nombre="Tacos de Cochinita Pibil", descripcion="Auténticos tacos mexicanos", precio=12.5, esta_en_carta=True, id_categoria="cat1"),
                Plato(id_plato="mock2", nombre="Hamburguesa Trufada", descripcion="Carne madurada, queso y mayonesa de trufa", precio=15.0, esta_en_carta=True, id_categoria="cat2")
            ]
        return platos_db

    def obtener_menu_del_dia(self, fecha):
        return None  # A implementar
