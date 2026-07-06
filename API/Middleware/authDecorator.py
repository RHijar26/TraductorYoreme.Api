from functools import wraps
from flask import request, jsonify, g
import jwt
from config import config

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'Token requerido'}), 401

        token = auth_header.split(' ')[1]    

        try:
            payload = jwt.decode(
                token,
                config.JW_SECRET_KEY,
                algorithms=[config.JW_ALGORITHM]
            )
            g.user_id = payload['user_id']
            g.user_role = payload['role']
            g.user_email = payload['email']
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'error': 'Token inválido'}), 401

        return f(*args, **kwargs)

    return decorated

def require_role(allowed_roles: list):
    def decorator(f):
        @wraps(f)
        @jwt_required  # primero autentica, luego verifica rol
        def decorated(*args, **kwargs):

            print(f"User role: {g.get('user_role')}, Allowed roles: {allowed_roles}")

            if g.get('user_role') not in allowed_roles:
                return jsonify({
                    'success': False,
                    'error': 'No tienes permisos para esta acción'
                }), 403
            return f(*args, **kwargs)
        return decorated
    return decorator