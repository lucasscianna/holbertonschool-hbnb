from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    """Resource for managing the list of amenities."""

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def post(self):
        """Ajouter une nouvelle amenity (Admin uniquement)"""
        # On récupère les claims du token
        claims = get_jwt()
        
        # Si le flag is_admin n'est pas présent ou est False -> 403
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload
        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    def get(self):
        """Retrieve a list of all amenities."""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """Resource for managing a specific amenity."""

    def get(self, amenity_id):
        """Get amenity details by ID."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    def put(self, amenity_id):
        """Modifier une amenity (Admin uniquement)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404
        return {'message': 'Amenity updated successfully'}, 200

