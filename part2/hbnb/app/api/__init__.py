"""
Initialisation de l'application Flask et configuration de l'API.
"""

from flask import Flask
from flask_restx import Api
from app.v1.users import api as users_ns


def create_app():
    """
    Crée et configure l'instance de l'application Flask.
    """
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    # On branche le quartier 'users' sur l'URL /api/v1/users
    api.add_namespace(users_ns, path='/api/v1/users')

    return app
