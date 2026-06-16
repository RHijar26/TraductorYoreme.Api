from flask import Blueprint, request, jsonify
from functools import wraps

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))


from DATABASE.repositories.phraseRepository import PhraseRepository
from DATABASE.db import db

phrase_bp = Blueprint('phrases', __name__, url_prefix='/phrases')

@phrase_bp.post('/register')
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
        required_fields = ['sourceLanguage', 'targetLanguage', 'regionId', 'modelId', 'phrase', 'traduction']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
            }), 400
        
        # Crear frase
        phrase, error = PhraseRepository.create(
            sourceLanguage=data['sourceLanguage'],
            targetLanguage=data['targetLanguage'],
            regionId=data['regionId'],
            modelId=data['modelId'],
            phrase=data['phrase'],
            traduction=data['traduction']
        )

        if error:
            # Determinar código de estado según el error
            status_code = 409 if 'ya está registrado' in error else 400
            return jsonify({
                'success': False,
                'error': error
            }), status_code
        
        #Frase creada exitosamente
        return jsonify({
            'success': True,
            'message': 'Frase registrada exitosamente',
            'data': phrase.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500
    

@phrase_bp.get('/')
def get_all():
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 100, type=int)
        phrases = PhraseRepository.get_all(page, page_size)    

        return jsonify({
            'success': True,
            'data': [{k[0].lower() + k[1:]: v for k, v in phrase.items()} for phrase in phrases],
            'page': page,
            'pageSize': page_size
            
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500