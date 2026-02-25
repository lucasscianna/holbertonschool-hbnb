from flask import Flask
from flask_restx import Api

def create_app():
    """
    Initialise l'application Flask et enregistre les namespaces de l'API.
    """
    app = Flask(__name__)
    
    # On importe le blueprint défini dans app/api/v1/__init__.py
    from app.api.v1 import blueprint as api_v1
    app.register_blueprint(api_v1)
    
    return app
