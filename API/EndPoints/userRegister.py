import uuid

from flask import Blueprint, request, jsonify
from functools import wraps

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))


from API.services.mailService import send_welcome_email
from DATABASE.repositories.userRegisterRepository import UserRegisterRepository
from DATABASE.repositories.userRepository import UserRepository
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
    
@user_register_bp.put('/approve/<int:user_register_id>')
def approve(user_register_id: int):
    try:                  
        token = str(uuid.uuid4())
        
        user_update = UserRegisterRepository.approve(
            user_register_id,
            token
        )        

        if not user_update:
            return jsonify({'success': False, 'error': "No se pudo aprobar el usuario"}), 500                
        

        send_welcome_email(user_update.Email, user_update.Name,token)  # Enviar correo de bienvenida al usuario aprobado

        return jsonify({
            'success': True,
            'message': 'Usuario aprobado y correo de confirmación enviado.'
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
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
    
@user_register_bp.get('/pending')
def get_pending():
    try:
        pending_count = UserRegisterRepository.get_pending()
        return jsonify({
            'success': True,
            'data': pending_count
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@user_register_bp.put('/decline/<int:user_register_id>')
def decline(user_register_id: int):
    try:
        user_register = UserRegisterRepository.decline(user_register_id)
        if not user_register:
            return jsonify({
                'success': False,
                'error': 'Registro de usuario no encontrado'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Registro de usuario declinado exitosamente',
            'data': user_register.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@user_register_bp.post('/setPassword')
def set_password():
    try:
        data = request.get_json()             
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Validar campos requeridos
        required_fields = ['token', 'password']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
            }), 400
        
        user_register = UserRegisterRepository.get_by_token(data['token'])
        
        if not user_register:
            return jsonify({
                'success': False,
                'error': 'Token inválido o expirado'
            }), 400

        user, error = UserRepository.create(
            email=user_register.Email,
            password=data['password'],
            name=user_register.Name,
            last_name=user_register.LastName,
            second_last_name=user_register.SecondLastName
        )
        
        if error:            
            status_code = 409 if 'ya está registrado' in error else 400
            return jsonify({
                'success': False,
                'error': error
            }), status_code
        
        user_decline = UserRegisterRepository.decline(user_register.Id)  
        if not user_decline:
            return jsonify({
                'success': False,
                'error': 'Registro de usuario no encontrado'
            }), 404
        
        # Usuario creado exitosamente
        return jsonify({
            'success': True,
            'message': 'Usuario registrado exitosamente, bienvenido a la plataforma!',
        }), 201        


        return jsonify({
            'success': True,
            'message': 'Token recibido, aquí se implementaría la lógica para establecer la contraseña.'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500