from flask import Blueprint, request, jsonify
from src.use_cases.dish_use_cases import ManageDishesUseCase
from src.infrastructure.database.mongo_repos import MongoDishRepository

dish_bp = Blueprint('dishes', __name__)

@dish_bp.route('/', methods=['POST'])
def add_dish():
    repo = MongoDishRepository()
    use_case = ManageDishesUseCase(repo)
    dish = use_case.create_dish(request.json)
    return jsonify({"message": "Plato creado", "id": dish.id}), 201

@dish_bp.route('/', methods=['GET'])
def get_dishes():
    repo = MongoDishRepository()
    use_case = ManageDishesUseCase(repo)
    dishes = use_case.list_dishes()
    return jsonify([d.__dict__ for d in dishes]), 200

@dish_bp.route('/<id>', methods=['DELETE'])
def delete_dish(id):
    repo = MongoDishRepository()
    use_case = ManageDishesUseCase(repo)
    use_case.remove_dish(id)
    return jsonify({"message": "Plato eliminado"}), 200