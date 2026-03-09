from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the data expected during registration/update
user_request = api.model('UserRegistration', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password')
})

# Define the data returned to the client (password is excluded)
user_response = api.model('UserResponse', {
    'id': fields.String(description='Unique identifier'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email address')
})

@api.route('/')
class UserList(Resource):
    """Handles actions on the complete user collection."""

    @api.expect(user_request, validate=True)
    @api.marshal_with(user_response, code=201)
    def post(self):
        """Creates a new user and returns the filtered public profile."""
        user_data = api.payload
        try:
            new_user = facade.create_user(user_data)
            return new_user
        except ValueError as e:
            api.abort(400, str(e))

    @api.marshal_list_with(user_response)
    def get(self):
        """Retrieves all registered users."""
        return facade.get_all_users()

@api.route('/<user_id>')
class UserResource(Resource):
    """Handles actions on a specific user."""

    @api.marshal_with(user_response)
    def get(self, user_id):
        """Retrieves a specific user by their unique identifier."""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user

    @api.expect(user_request, validate=True)
    def put(self, user_id):
        """Updates an existing user's information."""
        user_data = api.payload
        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                api.abort(404, "User not found")
            return {'message': 'User updated successfully'}, 200
        except ValueError as e:
            api.abort(400, str(e))