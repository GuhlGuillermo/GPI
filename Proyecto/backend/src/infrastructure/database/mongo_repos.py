import pymongo
from flask import current_app
from src.domain.models import Order, User, OrderPricing, OrderItem

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
