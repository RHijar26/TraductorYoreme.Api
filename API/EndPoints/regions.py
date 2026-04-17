from flask import Blueprint, request, jsonify
from functools import wraps

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.repositories.regionRepository import RegionRepository
from DATABASE.db import db


regions_bp = Blueprint('regions', __name__, url_prefix='/regions')
@regions_bp.post('/register')
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
        
        # Crear Region
        region, error = RegionRepository.create(
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
        
        #Region creada exitosamente
        return jsonify({
            'success': True,
            'message': 'Región registrada exitosamente',
            'data': region.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500

@regions_bp.get('/')
def get_all():   
    try:
        regions = RegionRepository.get_all()
        return jsonify({
            'success': True,
            'data': [region.to_dict() for region in regions]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500

@regions_bp.delete('/<int:region_id>')
def delete(region_id):
    try:
        success, error = RegionRepository.delete(region_id)
        if not success:
            status_code = 404 if 'no encontrada' in error else 400
            return jsonify({
                'success': False,
                'error': error
            }), status_code
        
        return jsonify({
            'success': True,
            'message': 'Región eliminada exitosamente'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500