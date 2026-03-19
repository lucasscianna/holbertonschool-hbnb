from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='Opérations sur les utilisateurs')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='Prénom'),
    'last_name': fields.String(required=True, description='Nom'),
    'email': fields.String(required=True, description='Adresse email'),
    'password': fields.String(required=True, description='Mot de passe')
})

@api.route('/')
class UserList(Resource):

    def post(self):
        """Inscription ouverte. Le 1er user créé devient admin automatiquement."""
        user_data = api.payload
        if not user_data:
            return {'error': 'Données manquantes'}, 400

        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

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

    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'Utilisateur non trouvé'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    def put(self, user_id):
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'Utilisateur non trouvé'}, 404

        if not is_admin and user_id != current_user_id:
            return {'error': 'Action non autorisée'}, 403

        user_data = api.payload
        if not user_data:
            return {'error': 'Données manquantes'}, 400

        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'Seul un admin peut modifier email ou mot de passe'}, 400

        if is_admin and 'email' in user_data:
            existing = facade.get_user_by_email(user_data['email'])
            if existing and existing.id != user_id:
                return {'error': 'Email already in use'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)  #récupère l'objet
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200  #retourne les données au lieu du message
        except ValueError as e:
            return {'error': str(e)}, 400