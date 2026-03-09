from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='Opérations sur les utilisateurs')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Prénom'),
    'last_name': fields.String(required=True, description='Nom'),
    'email': fields.String(required=True, description='Adresse email')
    'password': fields.String(required=True, description='Mot de passe')
})

@api.route('/')
class UserList(Resource):
    """
    Gère les actions sur la collection complète des utilisateurs.
    """

    @api.expect(user_model, validate=True)
    def post(self):
        """
        Crée un nouvel utilisateur après validation.
        """
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

    def get(self):
        """
        Récupère tous les utilisateurs enregistrés.
        """
        users = facade.get_all_users()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            } for u in users
        ], 200

@api.route('/<user_id>')
class UserResource(Resource):
    """
    Gère les actions sur un utilisateur spécifique.
    """

    def get(self, user_id):
        """
        Récupère un utilisateur précis via son identifiant unique.
        """
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
    def put(self, user_id):
        """
        Met à jour les informations d'un utilisateur existant.
        """
        user_data = api.payload
        
        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'Utilisateur non trouvé'}, 404
            return {'message': 'Utilisateur mis à jour avec succès'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
    