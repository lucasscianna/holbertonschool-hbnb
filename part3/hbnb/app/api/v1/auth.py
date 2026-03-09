from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Login model for input validation in Swagger
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """Authenticate user and return a JWT token"""
        auth_data = api.payload
        
        # 1. Retrieve user by email
        user = facade.get_user_by_email(auth_data['email'])
        
        # 2. Check if user exists and password is correct
        # verify_password() uses bcrypt under the hood
        if not user or not user.verify_password(auth_data['password']):
            return {'error': 'Invalid credentials'}, 401

        # 3. Generate the access token
        # identity is typically the user's unique ID
        # is_admin is added as a claim for easy authorization checks later
        access_token = create_access_token(
            identity=user.id, 
            additional_claims={"is_admin": user.is_admin}
        )
        
        return {'access_token': access_token}, 200