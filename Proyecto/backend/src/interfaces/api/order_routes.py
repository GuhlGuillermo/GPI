from flask import Blueprint, request, jsonify
from src.use_cases.order_use_cases import CreateOrderUseCase, GetOrdersUseCase
from src.infrastructure.database.mongo_repos import MongoOrderRepository, MongoUserRepository
from src.domain.exceptions import BusinessRuleException

order_bp = Blueprint('orders', __name__)

@order_bp.route('/', methods=['GET'])
def get_orders():
    """
    Ruta para que el administrador/dashboard consulte el listado de pedidos en tiempo real.
    """
    order_repo = MongoOrderRepository()
    use_case = GetOrdersUseCase(order_repo=order_repo)
    
    try:
        orders = use_case.execute()
        orders_list = []
        for o in orders:
            orders_list.append({
                "id_pedido": o.id_pedido,
                "id_usuario": o.id_usuario,
                "importe_total": o.importe_total,
                "estado": o.estado,
                "dir_entrega": o.dir_entrega,
                "hora_entrega": o.hora_entrega.isoformat() if o.hora_entrega else None,
                "info_pago": o.info_pago,
                "origen_dato": getattr(o, 'origen_dato', 'Desconocido'),
                "items": [{"id_plato": i.id_plato, "nombre_plato": i.nombre_plato, "precio_plato": i.precio_plato, "cantidad": i.cantidad} for i in o.items]
            })
        return jsonify(orders_list), 200
    except Exception as e:
        return jsonify({"error": "Error al recuperar pedidos", "details": str(e)}), 500

@order_bp.route('/', methods=['POST'])
def create_order():
    """
    Ruta que expone el endpoint al mundo. Recibe JSON desde React, 
    compone el entorno estricto inyectando las dependencias de Mongo a los UsesCases.
    """
    data = request.get_json()
    
    # 1. Extracción e intercepción simple de payload HTTP
    id_usuario = data.get('id_usuario', 'invitado')
    items_data = data.get('items', [])
    credit_card = data.get('credit_card', "")
    dir_entrega = data.get('dir_entrega', "")
    nombre = data.get('nombre', "")
    email = data.get('email', "")
    ignore_schedule = data.get('ignore_schedule', False)
    
    # 2. Inyección de dependencias (Conectamos la Capa 4 a la Capa 2)
    order_repo = MongoOrderRepository()
    user_repo = MongoUserRepository()
    
    use_case = CreateOrderUseCase(order_repo=order_repo, user_repo=user_repo)
    
    try:
        # Aquí cruzamos a la pura lógica de negocio
        order = use_case.execute(
            user_id=id_usuario, 
            items_data=items_data, 
            credit_card=credit_card, 
            dir_entrega=dir_entrega, 
            nombre=nombre, 
            email=email,
            ignore_schedule=ignore_schedule
        )
        
        return jsonify({
            "message": "Pedido recibido correctamente. El cocinero ha sido notificado.",
            "id_pedido": order.id_pedido,
            "estado": order.estado,
            "importe_total": order.importe_total
        }), 201

    except BusinessRuleException as business_error:
        # Atrapamos violaciones de negocio como Mínimo de 15€, Horarios o Tarjetas falsas.
        return jsonify({"error": str(business_error)}), 400
    except Exception as e:
        # Fallos internos catastróficos del sistema (BD caída, etc)
        return jsonify({"error": "Error interno del servidor.", "details": str(e)}), 500
