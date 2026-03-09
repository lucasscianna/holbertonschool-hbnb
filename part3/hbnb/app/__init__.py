from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    # On ajoute cette ligne pour charger les réglages du fichier config.py
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    
    api = Api(app,
            version='1.0',
            title='HBnB API',
            description='HbnB Application API',
            doc='/api/V1/')
    
    from app.api.v1 import blueprint as api_v1
    app.register_blueprint(api_v1)

    return app