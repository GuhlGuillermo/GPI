from flask import Blueprint, request, jsonify
from app.db import menus

menus_bp = Blueprint("menus", __name__)

# Crear menú
@menus_bp.route("/menus", methods=["POST"])
def crear_menu():
    data = request.json

    required = ["fecha", "entrantes", "principales", "postres"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Falta {field}"}), 400

    menus.insert_one(data)
    return jsonify({"message": "Menú creado"}), 201


# Obtener menú por fecha
@menus_bp.route("/menus/<fecha>", methods=["GET"])
def get_menu(fecha):
    menu = menus.find_one({"fecha": fecha})

    if not menu:
        return jsonify({"message": "No hay menú para esta fecha"}), 404

    menu["_id"] = str(menu["_id"])
    return jsonify(menu)