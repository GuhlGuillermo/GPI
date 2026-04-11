from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class UserRole(Enum):
    CLIENT = "CLIENT"
    CHEF = "CHEF"
    DELIVERY = "DELIVERY"
    OWNER = "OWNER"
    
@dataclass
class DailyMenuSelection:
    menu_date: str
    snapshot_price: float
    selected_starter: str
    selected_main: str
    selected_dessert: str

@dataclass
class OrderItem:
    dish_id: str
    name: str # Snapshot inmutable
    snapshot_price: float
    quantity: int

@dataclass
class OrderPricing:
    subtotal: float
    loyalty_discount_applied: float = 0.0
    
    @property
    def total(self) -> float:
        return max(0.0, self.subtotal - self.loyalty_discount_applied)

@dataclass
class Order:
    id: str
    user_id: str
    items: List[OrderItem] = field(default_factory=list)
    daily_menu_selections: List[DailyMenuSelection] = field(default_factory=list)
    pricing: OrderPricing = None
    status: str = "RECEIVED"
    created_at: datetime = field(default_factory=datetime.now)

    def can_be_modified(self) -> bool:
        """Verifica si han pasado menos de 10 minutos desde la creación [cite: 34]"""
        from datetime import datetime, timedelta
        limit = self.created_at + timedelta(minutes=10)
        return datetime.now() <= limit

@dataclass
class User:
    id: str
    role: UserRole  # Cliente, Chef, Delivery o Owner
    historial_gasto_total: float = 0.0

@dataclass
class Dish:
    id: str
    name: str
    description: str
    price: float
    category: str  # entrantes, ensaladas, tandoori, bebidas, etc.
    season: str    # primavera, verano, otoño, invierno o todo el año

@dataclass
class DailyMenuConfig:
    date: str  # Formato "YYYY-MM-DD"
    starters: List[str]  # Exactamente 3 nombres/IDs de platos 
    mains: List[str]     # Exactamente 3 nombres/IDs de platos 
    desserts: List[str]  # Exactamente 2 nombres/IDs de platos 
    price: float = 15.0  # Precio fijo
