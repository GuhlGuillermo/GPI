import pymongo
from flask import current_app
from src.domain.models import Order, User, OrderItem, Dish, Menu

def get_db():
    client = pymongo.MongoClient(current_app.config['MONGO_URI'])
    return client.get_default_database() if client.get_default_database().name else client['sabor_del_himalaya']

class MongoOrderRepository:
    """Implementación de persistencia para Pedidos"""
    
    def __init__(self):
        self.collection = get_db()['pedidos'] # Renombro colección a 'pedidos' por consistencia
    
    def save(self, order: Order) -> None:
        data = {
            '_id': order.id_pedido,
            'id_usuario': order.id_usuario,
            'importe_total': order.importe_total,
            'estado': order.estado,
            'dir_entrega': order.dir_entrega,
            'hora_entrega': order.hora_entrega,
            'info_pago': order.info_pago,
            'items': [
                {
                    'id_plato': item.id_plato,
                    'nombre_plato': item.nombre_plato,
                    'precio_plato': item.precio_plato,
                    'cantidad': item.cantidad
                } for item in order.items
            ]
        }
        self.collection.update_one({'_id': order.id_pedido}, {'$set': data}, upsert=True)

class MongoUserRepository:
    """Implementación de persistencia para Usuarios"""
    
    def __init__(self):
        self.collection = get_db()['usuarios'] # Renombro colección
        
    def get_by_id(self, user_id: str) -> User | None:
        data = self.collection.find_one({'_id': user_id})
        if not data:
            return None
        return User(
            id_usuario=str(data['_id']),
            nombre=data.get('nombre', ''),
            email=data.get('email', ''),
            contraseña=data.get('contraseña', ''),
            gasto_total=data.get('gasto_total', 0.0),
            es_cliente_habitual=data.get('es_cliente_habitual', False),
            rol=data.get('rol', 'CLIENT')
        )
        
    def get_by_email(self, email: str) -> User | None:
        data = self.collection.find_one({'email': email})
        if not data:
            return None
        return User(
            id_usuario=str(data['_id']),
            nombre=data.get('nombre', ''),
            email=data.get('email', ''),
            contraseña=data.get('contraseña', ''),
            gasto_total=data.get('gasto_total', 0.0),
            es_cliente_habitual=data.get('es_cliente_habitual', False),
            rol=data.get('rol', 'CLIENT')
        )
        
    def save(self, user: User) -> None:
        data = {
            '_id': user.id_usuario,
            'nombre': user.nombre,
            'email': user.email,
            'contraseña': user.contraseña,
            'gasto_total': user.gasto_total,
            'es_cliente_habitual': user.es_cliente_habitual,
            'rol': user.rol
        }
        self.collection.update_one({'_id': user.id_usuario}, {'$set': data}, upsert=True)

from typing import List

class MongoDishRepository:
    """Implementación de persistencia para Platos"""
    
    def __init__(self):
        self.collection = get_db()['platos'] # Colección platos
        
    def save(self, dish: Dish) -> None:
        data = {
            '_id': dish.id_plato,
            'nombre_plato': dish.nombre_plato,
            'descripcion': dish.descripcion,
            'precio_plato': dish.precio_plato,
            'categoria': dish.categoria,
            'es_de_temporada': dish.es_de_temporada,
            'url_imagen': dish.url_imagen,
            'activo': dish.activo
        }
        self.collection.update_one({'_id': dish.id_plato}, {'$set': data}, upsert=True)
        
    def get_by_id(self, dish_id: str):
        data = self.collection.find_one({'_id': dish_id})
        if not data: return None
        return Dish(
            id_plato=str(data['_id']),
            nombre_plato=data['nombre_plato'],
            descripcion=data.get('descripcion', ''),
            precio_plato=data['precio_plato'],
            categoria=data['categoria'],
            es_de_temporada=data.get('es_de_temporada', False),
            url_imagen=data.get('url_imagen', ''),
            activo=data.get('activo', True)
        )
        
    def get_all(self, active_only: bool = True) -> List[Dish]:
        query = {'activo': True} if active_only else {}
        cursor = self.collection.find(query)
        return [
            Dish(
                id_plato=str(d['_id']),
                nombre_plato=d['nombre_plato'],
                descripcion=d.get('descripcion', ''),
                precio_plato=d['precio_plato'],
                categoria=d['categoria'],
                es_de_temporada=d.get('es_de_temporada', False),
                url_imagen=d.get('url_imagen', ''),
                activo=d.get('activo', True)
            ) for d in cursor
        ]

class MongoMenuRepository:
    """Implementación de persistencia para Menú"""
    
    def __init__(self):
        self.collection = get_db()['menu'] # Colección menú
        
    def save(self, menu: Menu) -> None:
        data = {
            '_id': menu.id_menu,
            'fecha': menu.fecha,
            'entrantes': menu.entrantes,
            'platos_principal': menu.platos_principal,
            'postres': menu.postres,
            'precio_menu': menu.precio_menu
        }
        self.collection.update_one({'_id': menu.id_menu}, {'$set': data}, upsert=True)
        
    def get_by_date(self, fecha: str) -> Menu | None:
        data = self.collection.find_one({'fecha': fecha})
        if not data: return None
        return Menu(
            id_menu=str(data['_id']),
            fecha=data['fecha'],
            entrantes=data.get('entrantes', []),
            platos_principal=data.get('platos_principal', []),
            postres=data.get('postres', []),
            precio_menu=data.get('precio_menu', 0.0)
        )
