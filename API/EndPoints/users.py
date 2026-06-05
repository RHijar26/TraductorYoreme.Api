from flask import Blueprint, request, jsonify
from functools import wraps

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.repositories.userRepository import UserRepository
from DATABASE.db import db

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.post('/register')
def register():    
    try:
        # Obtener datos del request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Validar campos requeridos
        required_fields = ['email', 'password', 'name', 'lastName', 'secondLastName']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
            }), 400
        
        # Crear usuario
        user, error = UserRepository.create(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            last_name=data['lastName'],
            second_last_name=data['secondLastName']
        )
        
        if error:
            # Determinar código de estado según el error
            status_code = 409 if 'ya está registrado' in error else 400
            return jsonify({
                'success': False,
                'error': error
            }), status_code
        
        # Usuario creado exitosamente
        return jsonify({
            'success': True,
            'message': 'Usuario registrado exitosamente',
        }), 201
    
    except Exception as e:        
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@users_bp.get('/')
def get_all():
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 100, type=int)
        active_only = request.args.get('activeOnly', 'true').lower() == 'true'

        if page < 1 or page_size < 1:
            return jsonify({
                'success': False,
                'error': 'Los parámetros page y pageSize deben ser mayores a 0'
            }), 400

        users = UserRepository.get_all(active_only=active_only, page=page, page_size=page_size)

        return jsonify({
            'success': True,
            'data': [{k[0].lower() + k[1:]: v for k, v in user.items()} for user in users],
            'page': page,
            'pageSize': page_size
            
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }), 500
