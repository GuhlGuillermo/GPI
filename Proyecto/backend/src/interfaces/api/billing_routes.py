from flask import Blueprint, jsonify
from src.use_cases.billing_buffer import BillingBufferManager

billing_bp = Blueprint('billing', __name__)

@billing_bp.route('/today', methods=['GET'])
def get_today_billing():
    """
    Ruta para que el Chef consulte en vivo la facturación.
    Combina lo grabado en Mongo con lo que aún está retenido en la RAM.
    """
    manager = BillingBufferManager()
    snapshot = manager.get_current_snapshot()
    return jsonify(snapshot), 200

@billing_bp.route('/flush', methods=['POST'])
def flush_billing():
    """
    Fuerza un Cierre de Caja manual volcando la RAM a MongoDB.
    Ideal para llamar al cerrar el restaurante.
    """
    manager = BillingBufferManager()
    manager.flush_to_db()
    return jsonify({"message": "Cierre de caja completado. Memoria RAM liberada y datos volcados a MongoDB."}), 200
