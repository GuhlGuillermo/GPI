import os
from flask import Flask, jsonify
from flask_cors import CORS
from src.interfaces.api.order_routes import order_bp
from src.interfaces.api.auth_routes import auth_bp
from src.interfaces.api.dish_routes import dish_bp
from src.interfaces.api.menu_routes import menu_bp

def create_app():
    """Factory para instanciar el servidor Flask bajo Clean Architecture"""
    app = Flask(__name__)
    
    # Configuramos variables globales que después se extraerían de un archivo config o .env
    app.config['MONGO_URI'] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/sabor_del_himalaya")
    app.config['JWT_SECRET_KEY'] = "super-secret-changeme"
    
    CORS(app) # Permitiremos peticiones del Frontend React (Origins = '*')

    # Registrar Interfaces / Endpoints Modulares (Blueprints)
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(dish_bp, url_prefix='/api/dishes')
    app.register_blueprint(menu_bp, url_prefix='/api/menu')

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "OK", "message": "Sabor del Himalaya API Running"}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
