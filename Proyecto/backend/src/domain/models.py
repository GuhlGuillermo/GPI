from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

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

@dataclass
class User:
    id: str
    role: str # CLIENT, CHEF...
    historial_gasto_total: float = 0.0
