from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Opérations d\'authentification')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """Authentifie l'utilisateur et renvoie un token JWT"""
        auth_data = api.payload
        
        # 1. Chercher l'utilisateur
        user = facade.get_user_by_email(auth_data['email'])
        
        # 2. Vérifier l'existence et le mot de passe (via la méthode du modèle User)
        if not user or not user.verify_password(auth_data['password']):
            return {'error': 'Identifiants invalides'}, 401

        # 3. Générer le token avec des infos utiles (claims)
        access_token = create_access_token(
            identity=user.id, 
            additional_claims={"is_admin": user.is_admin}
        )
        
        return {'access_token': access_token}, 200