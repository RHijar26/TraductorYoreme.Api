import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS

from flask import Flask
from flask_mail import Mail

import sys
from pathlib import Path
# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from API.services.mailService import send_welcome_email
from config import config 

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend applications (Angular, React, etc.)

from DATABASE.db import init_db
init_db(app)


app.config['MAIL_SERVER'] = config.mail_server
app.config['MAIL_PORT'] = config.mail_port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config.mail_username
app.config['MAIL_PASSWORD'] = config.mail_password
mail = Mail()
mail.init_app(app) # This initializes the email service

mail.default_sender = config.mail_username  # Set the default sender email address


import API.EndPoints.users as users
import API.EndPoints.models as models
import API.EndPoints.auth as auth
import API.EndPoints.regions as regions
import API.EndPoints.lenguage as lenguage
import API.EndPoints.phrase as phrase
import API.EndPoints.userRegister as userRegister


# Registrar blueprints
app.register_blueprint(users.users_bp)  # /api/users/*
app.register_blueprint(models.models_bp)  # /api/models/*
app.register_blueprint(regions.regions_bp)  # /api/regions/*
app.register_blueprint(auth.auth_bp)  # /api/auth/*
app.register_blueprint(lenguage.lenguage_bp)  # /api/lenguage/*
app.register_blueprint(phrase.phrase_bp)  # /api/phrases
app.register_blueprint(userRegister.user_register_bp)  # /api/userRegister/*

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


@app.get("/mail")
def register():

    print("Simulating user registration...")

    # ... logic to save user to DB ...
    user_email = "jesusroberto.hijarangulo.01@gmail.com"
    user_name = "John Doe"
    token = str(uuid.uuid4())

    send_welcome_email(user_email, user_name, token)
    return "Check your inbox!"


if __name__ == '__main__':
    app.run(
        host=config.api_host,
        port=config.api_port,
        debug=config.app_debug
    )

