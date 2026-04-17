from flask import Flask, request, jsonify
from flask_cors import CORS

import sys
from pathlib import Path

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from config import config 

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend applications (Angular, React, etc.)

from DATABASE.db import init_db
init_db(app)

import API.EndPoints.users as users
import API.EndPoints.models as models
import API.EndPoints.auth as auth
import API.EndPoints.regions as regions

# Registrar blueprints
app.register_blueprint(users.users_bp)  # /api/users/*
app.register_blueprint(models.models_bp)  # /api/models/*
app.register_blueprint(regions.regions_bp)  # /api/regions/*
app.register_blueprint(auth.auth_bp)  # /api/auth/*

#Translate methods
import TRANSLATE
import TRANSLATE.translate  
import TRANSLATE.normalize.normalize as normalize


@app.get("/Translate")
def home():    
    text = normalize.normalize(request.args.get('text', '')) 

    print("Texto a traducir:", text)

    translation = TRANSLATE.translate.translate(text)
    return  jsonify({"traduction": translation})

if __name__ == '__main__':
    app.run(
        host=config.api_host,
        port=config.api_port,
        debug=config.app_debug
    )
