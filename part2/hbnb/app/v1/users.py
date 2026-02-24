"""
Ce module contient les points d'entrée de l'API pour les utilisateurs.
Il gère les requêtes HTTP POST, GET et PUT pour l'entité User.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

# Définition du namespace pour regrouper les routes liées aux utilisateurs
api = Namespace('users', description='Opérations sur les utilisateurs')

# Modèle de données pour la documentation automatique Swagger et la validation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Prénom'),
    'last_name': fields.String(required=True, description='Nom'),
    'email': fields.String(required=True, description='Adresse email')
})


@api.route('/')
class UserList(Resource):
    """Gère les actions sur la collection complète des utilisateurs."""

    @api.expect(user_model, validate=True)
    @api.response(201, 'Utilisateur créé avec succès')
    @api.response(400, 'Données invalides ou email déjà utilisé')
    def post(self):
        """Crée un nouvel utilisateur après validation."""
        user_data = api.payload
        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Liste des utilisateurs récupérée avec succès')
    def get(self):
        """Récupère tous les utilisateurs enregistrés."""
        users = facade.get_all_users()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'email': u.email
            } for u in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    """Gère les actions sur un utilisateur spécifique identifié par son ID."""

    @api.response(200, 'Détails de l\'utilisateur récupérés')
    @api.response(404, 'Utilisateur non trouvé')
    def get(self, user_id):
        """Récupère un utilisateur précis via son identifiant unique."""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'Utilisateur non trouvé'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'Utilisateur mis à jour avec succès')
    @api.response(404, 'Utilisateur non trouvé')
    @api.response(400, 'Données de mise à jour invalides')
    def put(self, user_id):
        """Met à jour les informations d'un utilisateur existant."""
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'Utilisateur non trouvé'}, 404
        try:
            facade.update_user(user_id, user_data)
            return {'message': 'Utilisateur mis à jour avec succès'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
