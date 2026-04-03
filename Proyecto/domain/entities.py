from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, date

@dataclass
class Cliente:
    id_cliente: str
    registrado: bool
    direccion_guardada: str
    importe_consumido_acumulado: float

@dataclass
class Tarjeta_Credito:
    numero_16_digitos: str
    tipo_tarjeta: str

@dataclass
class Categoria:
    id_categoria: str
    nombre_categoria: str

@dataclass
class Plato:
    id_plato: str
    nombre: str
    descripcion: str
    precio: float
    esta_en_carta: bool
    id_categoria: str

@dataclass
class Menu_Diario:
    id_menu: str
    fecha_disponibilidad: date
    precio_fijo: float
    platos_ids: List[str] = field(default_factory=list)

@dataclass
class Personal:
    id_empleado: str
    rol_empleado: str

@dataclass
class Pedido:
    id_pedido: str
    id_cliente: str
    direccion_entrega: str
    hora_entrega_aprox: datetime
    estado: str  # e.g., 'Recibido', 'Preparando', 'En Camino', 'Entregado'
    importe_total: float
    id_empleado: Optional[str] = None
    tarjeta: Optional[Tarjeta_Credito] = None
    platos_ids: List[str] = field(default_factory=list)
    menus_ids: List[str] = field(default_factory=list)

