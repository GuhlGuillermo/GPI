from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.db import pedidos, platos

pedidos_bp = Blueprint("pedidos", __name__)


# Calcular total
def calcular_total(lista):
    total = 0

    for item in lista:
        plato = platos.find_one({"_id": ObjectId(item["plato_id"])})

        if not plato:
            continue

        total += plato["precio"] * item["cantidad"]

    return total


# Crear pedido
@pedidos_bp.route("/pedidos", methods=["POST"])
def crear_pedido():
    data = request.json

    if "platos" not in data or "direccion" not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    total = calcular_total(data["platos"])

    pedido = {
        "platos": data["platos"],
        "direccion": data["direccion"],
        "total": total
    }

    pedidos.insert_one(pedido)

    return jsonify({
        "message": "Pedido creado",
        "total": total
    }), 201