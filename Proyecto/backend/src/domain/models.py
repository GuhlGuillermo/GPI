from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class OrderItem:
    id_plato: str
    nombre_plato: str
    precio_plato: float
    cantidad: int

@dataclass
class Order:
    id_pedido: str
    id_usuario: str
    items: List[OrderItem] = field(default_factory=list)
    importe_total: float = 0.0
    estado: str = "RECIBIDO"
    dir_entrega: str = ""
    hora_entrega: Optional[datetime] = None
    info_pago: str = ""

@dataclass
class User:
    id_usuario: str
    nombre: str = ""
    email: str = ""
    contraseña: str = ""
    gasto_total: float = 0.0
    es_cliente_habitual: bool = False
    rol: str = "CLIENT"

@dataclass
class Dish:
    id_plato: str
    nombre_plato: str
    descripcion: str
    precio_plato: float
    categoria: str # "STARTER", "MAIN", "DESSERT" o "ENTRANTE", "PRINCIPAL", "POSTRE"
    es_de_temporada: bool = False
    url_imagen: str = ""
    activo: bool = True

    def __post_init__(self):
        if not self.url_imagen or self.url_imagen.strip() == "":
            self.url_imagen = "/default-dish.png"

@dataclass
class Menu:
    id_menu: str
    fecha: str
    entrantes: List[str] = field(default_factory=list)
    platos_principal: List[str] = field(default_factory=list)
    postres: List[str] = field(default_factory=list)
    precio_menu: float = 0.0
