from flask import Blueprint, request, jsonify,g
from functools import wraps

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from API.Middleware.authDecorator import jwt_required, require_role
from API.Enums.Roles import Roles

from DATABASE.repositories.phraseProposalRepository import PhraseProposalRepository
from DATABASE.repositories.phraseRepository import PhraseRepository
from DATABASE.db import db

hub_bp = Blueprint('hub', __name__, url_prefix='/hub')

@hub_bp.get('/')
@require_role([Roles.ADMINISTRATOR, Roles.TRANSLATOR])
def get_all():
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 100, type=int)
        phrases = PhraseRepository.get_hub_all(page, page_size)    

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

@hub_bp.get('/proposals')
@require_role([Roles.ADMINISTRATOR, Roles.TRANSLATOR])
def get_phrase_proposals():
    try:
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('pageSize', 100, type=int)
        phrase_id = request.args.get('phrase', type=int)
        phrases = PhraseProposalRepository.get_phrase_proposals(phrase_id, page, page_size)    

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

@hub_bp.post('/proposal')
@require_role([Roles.ADMINISTRATOR, Roles.TRANSLATOR])
def create_proposal():
    try:        
        author_id = g.user_id
        data = request.get_json()        
        required_fields = ['phrase', 'proposedText', 'reason']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
            }), 400

        new_proposal, error = PhraseProposalRepository.create(
            data['phrase'],            
            author_id,
            data['proposedText'], 
            data['reason'],
        )
        if error:
            return jsonify({
                'success': False,
                'error': error
            }), 400

        return jsonify({
            'success': True,
            'message': 'Propuesta creada exitosamente',
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        }), 500