from flask import Blueprint, request, jsonify
from functools import wraps

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.repositories.modelRepository import ModelRepository
from DATABASE.db import db

models_bp = Blueprint('models', __name__, url_prefix='/models')

@models_bp.post('/register')
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
        required_fields = ['name', 'description']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
            }), 400
        
        # Crear modelo
        model, error = ModelRepository.create(
            name=data['name'],
            description=data['description']
        )

        if error:
            # Determinar código de estado según el error
            status_code = 409 if 'ya está registrado' in error else 400
            return jsonify({
                'success': False,
                'error': error
            }), status_code
        
        #Modelo creado exitosamente
        return jsonify({
            'success': True,
            'message': 'Modelo registrado exitosamente',
            'data': model.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500
    
@models_bp.get('/')
def get_all():    
    try:
        models = ModelRepository.get_all()
        return jsonify({
            'success': True,
            'data': [model.to_dict() for model in models]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500
    
@models_bp.delete('/<int:model_id>')
def delete(model_id):
    print(f"Intentando eliminar modelo con ID: {model_id}")
    try:
        success, error = ModelRepository.delete(model_id)
        if not success:
            status_code = 404 if 'no encontrado' in error else 400
            return jsonify({
                'success': False,
                'error': error
            }), status_code
        
        return jsonify({
            'success': True,
            'message': 'Modelo eliminado exitosamente'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500