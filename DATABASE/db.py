from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    from config import config
    
    # Configurar SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = config.database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.sqlalchemy_track_modifications
    app.config['SQLALCHEMY_ECHO'] = config.database_echo

    # Inicializar extensiones
    db.init_app(app)    
                
    return db