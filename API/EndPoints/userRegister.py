from flask import Blueprint, request, jsonify
from functools import wraps

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))


from DATABASE.repositories.userRegisterRepository import UserRegisterRepository
from DATABASE.db import db

user_register_bp = Blueprint('userRegister', __name__, url_prefix='/userRegister')

@user_register_bp.post('/register')
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
        required_fields = ['email', 'name', 'lastName', 'secondLastName','aboutMe']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
            }), 400
        
        # Crear registro de usuario
        user_register, error = UserRegisterRepository.create(
            email=data['email'],
            name=data['name'],
            last_name=data['lastName'],
            second_last_name=data['secondLastName'],
            about_me=data.get('aboutMe')
        )
        
        if error:
            # Determinar código de estado según el error
            status_code = 409 if 'ya está registrado' in error else 400
            return jsonify({
                'success': False,
                'error': error
            }), status_code
        
        # Registro de usuario creado exitosamente
        return jsonify({
            'success': True,
            'message': 'Registro de usuario creado exitosamente',
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@user_register_bp.get('/approve/<int:user_register_id>')
def approve(user_register_id: int):
    try:
        user_register = UserRegisterRepository.approve(user_register_id)
        if not user_register:
            return jsonify({
                'success': False,
                'error': 'Registro de usuario no encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Registro de usuario aprobado exitosamente',
            'data': user_register.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@user_register_bp.get('/')
def get_all():
    try:
        user_registers = UserRegisterRepository.get_all()
        return jsonify({
            'success': True,
            'data': [ur.to_dict() for ur in user_registers]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500    