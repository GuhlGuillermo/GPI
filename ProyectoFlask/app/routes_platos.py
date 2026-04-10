from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.db import platos


platos_bp = Blueprint("platos", __name__)

@platos_bp.route("/platos", methods=["POST"])
def crear_plato():
    try:
        # 📥 Datos del formulario
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        categoria = request.form.get("categoria")
        temporada = request.form.get("temporada")

        # 🖼️ Imagen
        imagen = request.files.get("imagen")

        # ✅ Validación
        if not all([nombre, descripcion, precio, categoria, temporada]):
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        # 📁 Guardar imagen (si existe)
        filename = None
        if imagen:
            import os
            UPLOAD_FOLDER = "static/images"

            # crear carpeta si no existe
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            filename = imagen.filename
            path = os.path.join(UPLOAD_FOLDER, filename)
            imagen.save(path)

        # 📦 Crear objeto
        plato = {
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": float(precio),
            "categoria": categoria,
            "temporada": temporada,
            "imagen": filename
        }

        # 💾 Guardar en Mongo
        platos.insert_one(plato)

        return jsonify({"message": "Plato creado"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Obtener todos
@platos_bp.route("/platos", methods=["GET"])
def get_platos():
    data = []
    for p in platos.find():
        p["_id"] = str(p["_id"])
        data.append(p)
    return jsonify(data)


# Obtener uno
@platos_bp.route("/platos/<id>", methods=["GET"])
def get_plato(id):
    plato = platos.find_one({"_id": ObjectId(id)})

    if not plato:
        return jsonify({"error": "Plato no encontrado"}), 404

    plato["_id"] = str(plato["_id"])
    return jsonify(plato)


# Actualizar
@platos_bp.route("/platos/<id>", methods=["PUT"])
def update_plato(id):
    data = request.json

    result = platos.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Plato no encontrado"}), 404

    return jsonify({"message": "Plato actualizado"})


# Eliminar
@platos_bp.route("/platos/<id>", methods=["DELETE"])
def delete_plato(id):
    result = platos.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Plato no encontrado"}), 404

    return jsonify({"message": "Plato eliminado"})
