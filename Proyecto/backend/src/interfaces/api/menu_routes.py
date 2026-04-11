from flask import Blueprint, request, jsonify
from src.use_cases.menu_use_cases import ConfigureDailyMenuUseCase, GetAvailableMenuUseCase
from src.infrastructure.database.mongo_repos import MongoDailyMenuRepository

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/daily/configure', methods=['POST'])
def configure_menu():
    """Ruta para que el Chef configure el menú del día [cite: 16]"""
    menu_repo = MongoDailyMenuRepository()
    use_case = ConfigureDailyMenuUseCase(menu_repo)
    data = request.json
    # Validación de las 3 opciones de entrante, 3 principales y 2 postres [cite: 15]
    use_case.execute(data)
    return jsonify({"message": "Menú configurado correctamente"}), 201

@menu_bp.route('/daily/<date>', methods=['GET'])
def get_menu(date):
    """Ruta para que el cliente consulte el menú [cite: 23]"""
    menu_repo = MongoDailyMenuRepository()
    use_case = GetAvailableMenuUseCase(menu_repo)
    menu = use_case.execute(date)
    
    if not menu:
        # El sistema debe informar si no está disponible [cite: 20]
        return jsonify({"message": "Menú no disponible para esta fecha o fuera de horario"}), 404
        
    return jsonify(menu), 200