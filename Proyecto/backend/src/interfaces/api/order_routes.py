from flask import Blueprint, request, jsonify
from src.use_cases.order_use_cases import CreateOrderUseCase
from src.infrastructure.database.mongo_repos import MongoOrderRepository, MongoUserRepository
from src.domain.exceptions import BusinessRuleException

order_bp = Blueprint('orders', __name__)

@order_bp.route('/', methods=['POST'])
def create_order():
    """
    Ruta que expone el endpoint al mundo. Recibe JSON desde React, 
    compone el entorno estricto inyectando las dependencias de Mongo a los UsesCases.
    """
    data = request.get_json()
    
    # 1. Extracción e intercepción simple de payload HTTP
    user_id = data.get('user_id') # En un caso real se deduciría de un token JWT
    items_data = data.get('items', [])
    credit_card = data.get('credit_card', "")
    
    # 2. Inyección de dependencias (Conectamos la Capa 4 a la Capa 2)
    order_repo = MongoOrderRepository()
    user_repo = MongoUserRepository()
    
    use_case = CreateOrderUseCase(order_repo=order_repo, user_repo=user_repo)
    
    try:
        # Aquí cruzamos a la pura lógica de negocio
        order = use_case.execute(user_id=user_id, items_data=items_data, credit_card=credit_card)
        
        return jsonify({
            "message": "Pedido recibido correctamente. El cocinero ha sido notificado.",
            "order_id": order.id,
            "status": order.status,
            "total_charged": order.pricing.total
        }), 201

    except BusinessRuleException as business_error:
        # Atrapamos violaciones de negocio como Mínimo de 15€, Horarios o Tarjetas falsas.
        return jsonify({"error": str(business_error)}), 400
    except Exception as e:
        # Fallos internos catastróficos del sistema (BD caída, etc)
        return jsonify({"error": "Error interno del servidor.", "details": str(e)}), 500
