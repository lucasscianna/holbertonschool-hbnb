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
    """
    Gère les actions sur la collection complète des utilisateurs.
    """

   @api.expect(user_model, validate=True)
    @jwt_required()
    def post(self):
        """
        Crée un nouvel utilisateur (Réservé aux Admins).
        """
        # Vérification Admin
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        try:
            # Vérifier si l'email existe déjà
            if facade.get_user_by_email(user_data['email']):
                return {'error': 'Email already registered'}, 400
                
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

   @jwt_required()
    @api.expect(user_model, validate=True)
    def put(self, user_id):
        """
        Met à jour un utilisateur (Admin peut tout modifier, User limité à son profil).
        """
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        is_admin = claims.get('is_admin', False)
        user_data = api.payload
        
        # Si PAS admin ET que l'ID ne correspond pas -> Interdit
        if not is_admin and user_id != current_user_id:
            return {'error': 'Action non autorisée'}, 403

        # Si PAS admin, on interdit la modif email/password
        if not is_admin:
            if 'email' in user_data or 'password' in user_data:
                return {'error': 'Seul un administrateur peut modifier l\'email ou le mot de passe'}, 400
        
        try:
            # Si c'est un admin qui change l'email la facade doit vérifier l'unicité
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'Utilisateur non trouvé'}, 404
            return {'message': 'Utilisateur mis à jour avec succès'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400