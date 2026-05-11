from flask import Blueprint, request, jsonify
from functools import wraps

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

from DATABASE.repositories.lenguageRepository import LenguageRepository
from DATABASE.db import db

lenguage_bp = Blueprint('lenguage', __name__, url_prefix='/lenguage')

@lenguage_bp.get('/')
def get_lenguages():
    try:
        lenguages = LenguageRepository.get_all()
        return jsonify([lenguage.to_dict() for lenguage in lenguages]), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Error al obtener lenguajes: {str(e)}"
        }), 500
