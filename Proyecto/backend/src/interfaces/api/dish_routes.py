import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
from src.use_cases.dish_use_cases import DishUseCases
from src.infrastructure.database.mongo_repos import MongoDishRepository

dish_bp = Blueprint('dishes', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads')
DEFAULT_IMAGE = "/default-dish.png"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@dish_bp.route('/<path:filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@dish_bp.route('/', methods=['GET'])
def get_dishes():
    repo = MongoDishRepository()
    use_cases = DishUseCases(repo)
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    dishes = use_cases.get_all_dishes(active_only=active_only)
    
    return jsonify([{
        'id_plato': d.id_plato,
        'nombre_plato': d.nombre_plato,
        'descripcion': d.descripcion,
        'precio_plato': d.precio_plato,
        'categoria': d.categoria,
        'es_de_temporada': d.es_de_temporada,
        'url_imagen': d.url_imagen,
        'activo': d.activo
    } for d in dishes]), 200

@dish_bp.route('/', methods=['POST'])
# @require_role('CHEF')  # Idealmente protegido, pero comento por si no está implementado
def create_dish():
    repo = MongoDishRepository()
    use_cases = DishUseCases(repo)
    
    nombre_plato = request.form.get('nombre_plato')
    descripcion = request.form.get('descripcion', '')
    precio_plato = float(request.form.get('precio_plato', 0.0))
    categoria = request.form.get('categoria', 'ENTRANTE')
    
    url_imagen = ""
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            # URL relativa que espera el frontend apuntando a la api de este servidor
            url_imagen = f"http://localhost:5000/api/dishes/{filename}"

    try:
        dish = use_cases.create_dish(nombre_plato, descripcion, precio_plato, categoria, url_imagen)
        return jsonify({'message': 'Dish created successfully', 'id_plato': dish.id_plato}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@dish_bp.route('/<dish_id>', methods=['PUT'])
# @require_role('CHEF')
def update_dish(dish_id):
    repo = MongoDishRepository()
    use_cases = DishUseCases(repo)
    
    updates = {}
    if 'nombre_plato' in request.form: updates['nombre_plato'] = request.form.get('nombre_plato')
    if 'descripcion' in request.form: updates['descripcion'] = request.form.get('descripcion')
    if 'precio_plato' in request.form: updates['precio_plato'] = float(request.form.get('precio_plato'))
    if 'categoria' in request.form: updates['categoria'] = request.form.get('categoria')
    if 'es_de_temporada' in request.form: updates['es_de_temporada'] = request.form.get('es_de_temporada') == 'true'
    
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            updates['url_imagen'] = f"http://localhost:5000/api/dishes/{filename}"
            
    try:
        use_cases.update_dish(dish_id, updates)
        return jsonify({'message': 'Dish updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@dish_bp.route('/<dish_id>', methods=['DELETE'])
# @require_role('CHEF')
def delete_dish(dish_id):
    repo = MongoDishRepository()
    use_cases = DishUseCases(repo)
    try:
        use_cases.delete_dish(dish_id)
        return jsonify({'message': 'Dish deleted (logical)'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
