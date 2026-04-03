from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities import Pedido, Plato, Menu_Diario

class PedidoRepository(ABC):
    @abstractmethod
    def guardar(self, pedido: Pedido) -> None:
        pass
        
    @abstractmethod
    def obtener_por_id(self, id_pedido: str) -> Optional[Pedido]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Pedido]:
        pass
        
    @abstractmethod
    def actualizar_estado(self, id_pedido: str, nuevo_estado: str, id_empleado: str) -> None:
        pass

class CatalogoRepository(ABC):
    @abstractmethod
    def listar_platos_en_carta(self) -> List[Plato]:
        pass
        
    @abstractmethod
    def obtener_menu_del_dia(self, fecha) -> Optional[Menu_Diario]:
        pass
