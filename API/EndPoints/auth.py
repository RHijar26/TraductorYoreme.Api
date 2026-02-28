from flask import Blueprint, request, jsonify
from functools import wraps

from datetime import datetime, timedelta
import jwt
from functools import wraps

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.repositories.userRepository import UserRepository
from DATABASE.db import db
from config import config


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():    
    # Manejar preflight OPTIONS (CORS)
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Obtener datos del request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Validar campos requeridos
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email y password son requeridos'
            }), 400
        
        # Autenticar usuario
        user, error = UserRepository.authenticate(email, password)
        
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 401
        
        # Generar token JWT
        token = generate_token(user)
        
        # Login exitoso
        return jsonify({                        
            'token': token,            
        }), 200
    
    except Exception as e:
        print(f"❌ Error en login: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500



def generate_token(user):
    """
    Genera un token JWT para el usuario.
    
    Args:
        user: Objeto User
    
    Returns:
        str: Token JWT
    """
    payload = {
        'user_id': user.Id,
        'email': user.Email,
        'exp': datetime.utcnow() + timedelta(hours=config.JW_TOKEN_EXPIRATION_TIME),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, config.JW_SECRET_KEY, algorithm=config.JW_ALGORITHM)
    return token
