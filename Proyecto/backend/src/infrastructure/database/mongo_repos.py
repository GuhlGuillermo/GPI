from typing import List, Optional

import pymongo
from flask import current_app
from src.domain.models import DailyMenuConfig, Dish, Order, User, OrderPricing, OrderItem

def get_db():
    client = pymongo.MongoClient(current_app.config['MONGO_URI'])
    # Si la URI ya llevaba base de datos parseada en el string
    return client.get_default_database() if client.get_default_database().name else client['sabor_del_himalaya']

class MongoOrderRepository:
    """Implementación de persistencia para Pedidos"""
    
    def __init__(self):
        # Al instanciarse, usamos el contexto activo de Flask para coger la URI
        self.collection = get_db()['orders']
    
    def save(self, order: Order) -> None:
        # Convertimos la estructura de la entidad a JSON Dictionary
        data = {
            '_id': order.id,
            'user_id': order.user_id,
            'status': order.status,
            'created_at': order.created_at,
            'pricing': {
                'subtotal': order.pricing.subtotal,
                'loyalty_discount_applied': order.pricing.loyalty_discount_applied,
                'total': order.pricing.total
            },
            'items': [
                {
                    'dish_id': item.dish_id,
                    'name': item.name,
                    'snapshot_price': item.snapshot_price,
                    'quantity': item.quantity
                } for item in order.items
            ]
        }
        
        # Upsert (Crea o actualiza si existe) para garantizar inmutabilidad
        self.collection.update_one({'_id': order.id}, {'$set': data}, upsert=True)

    def get_daily_turnover(self, date_str: str) -> float:
        """
        Calcula el total de ingresos para un día específico (formato YYYY-MM-DD).
        Filtra los pedidos por el campo 'created_at'.
        """
        from datetime import datetime, time
        
        # Convertimos el string de fecha a objetos datetime (inicio y fin del día)
        day = datetime.strptime(date_str, "%Y-%m-%d")
        start_of_day = datetime.combine(day, time.min)
        end_of_day = datetime.combine(day, time.max)
        
        # Consultamos todos los pedidos en ese rango de tiempo
        orders = self.collection.find({
            "created_at": {"$gte": start_of_day, "$lte": end_of_day}
        })
        
        # Sumamos el campo 'total' dentro del objeto 'pricing' de cada pedido
        return sum(order['pricing']['total'] for order in orders)

class MongoUserRepository:
    """Implementación de persistencia para Usuarios (y su fidelización)"""
    
    def __init__(self):
        self.collection = get_db()['users']
        
    def get_by_id(self, user_id: str) -> User | None:
        data = self.collection.find_one({'_id': user_id})
        if not data:
            return None
        return User(
            id=str(data['_id']),
            role=data.get('role', 'CLIENT'),
            historial_gasto_total=data.get('loyalty', {}).get('historial_gasto_total', 0.0)
        )
        
    def save(self, user: User) -> None:
        self.collection.update_one(
            {'_id': user.id}, 
            {'$set': {
                'role': user.role, 
                'loyalty.historial_gasto_total': user.historial_gasto_total
            }}, 
            upsert=True
        )

class MongoDailyMenuRepository:
    def __init__(self):
        self.collection = get_db()['daily_menus']

    def save(self, config: DailyMenuConfig):
        self.collection.update_one(
            {'date': config.date},
            {'$set': {
                'starters': config.starters,
                'mains': config.mains,
                'desserts': config.desserts,
                'price': config.price
            }},
            upsert=True
        )

    def get_by_date(self, date_str: str) -> DailyMenuConfig | None:
        data = self.collection.find_one({'date': date_str})
        if not data:
            return None
        return DailyMenuConfig(
            date=data['date'],
            starters=data['starters'],
            mains=data['mains'],
            desserts=data['desserts'],
            price=data.get('price', 15.0)
        )

class MongoDishRepository:
    def __init__(self):
        # Usamos una propiedad o lo instanciamos dentro para evitar errores de contexto
        pass

    @property
    def collection(self):
        return get_db()['dishes']

    def save(self, dish: Dish) -> None:
        data = {
            'name': dish.name,
            'description': dish.description,
            'price': dish.price,
            'category': dish.category,
            'season': dish.season
        }
        self.collection.update_one({'_id': dish.id}, {'$set': data}, upsert=True)

    def get_all(self) -> List[Dish]:
        docs = self.collection.find()
        return [Dish(id=str(d['_id']), **{k: v for k, v in d.items() if k != '_id'}) for d in docs]

    def delete(self, dish_id: str) -> None:
        self.collection.delete_one({'_id': dish_id})
        
    def get_by_id(self, dish_id: str) -> Optional[Dish]:
        d = self.collection.find_one({'_id': dish_id})
        if not d: return None
        return Dish(id=str(d['_id']), **{k: v for k, v in d.items() if k != '_id'})