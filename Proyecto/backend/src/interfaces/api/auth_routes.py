from flask import Blueprint, request, jsonify, current_app
import jwt
from datetime import datetime, timedelta

# En Python moderno para seguridad usaríamos librerías puras de criptografía. 
# En este PoC comprobamos un secreto básico harcodeado.
SECRET_CHEF_PASSWORD = "himalayasecret"

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Valida la contraseña y emite un token JWT si el rol es CHEF."""
    data = request.get_json()
    
    role = data.get('role')
    secret = data.get('secret_key')
    
    if role == "CHEF" and secret == SECRET_CHEF_PASSWORD:
        # Emitir Token JWT válido por 12 horas
        expiration = datetime.utcnow() + timedelta(hours=12)
        token = jwt.encode(
            {
                "sub": "chef_account",
                "role": "CHEF",
                "exp": expiration
            },
            current_app.config['JWT_SECRET_KEY'],
            algorithm="HS256"
        )
        return jsonify({"token": token, "message": "Acceso de Chef concedido"}), 200
        
    return jsonify({"error": "Credenciales inválidas"}), 401
