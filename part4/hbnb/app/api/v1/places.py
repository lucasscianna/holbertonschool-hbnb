from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(),
    'name': fields.String()
})

user_model = api.model('PlaceUser', {
    'id': fields.String(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String()
})

review_model_summary = api.model('PlaceReview', {
    'id': fields.String(),
    'text': fields.String(),
    'rating': fields.Integer(),
    'user_id': fields.String()
})

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'country': fields.String(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String)
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            data = api.payload
            data['owner_id'] = current_user_id
            new_place = facade.create_place(data)
            return {'id': new_place.id, 'title': new_place.title, 'owner_id': new_place.owner.id}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        return [{'id': p.id, 'title': p.title, 'latitude': p.latitude, 'longitude': p.longitude, 'country': p.country} for p in facade.get_all_places()], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id, 'title': place.title, 'description': place.description,
            'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude,
            'country': place.country,
            'owner': {'id': place.owner.id, 'first_name': place.owner.first_name, 'email': place.owner.email},
            'amenities': [{'id': a.id, 'name': a.name} for a in place.amenities],
            'reviews': [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in place.reviews]
        }, 200

    @jwt_required()
    def put(self, place_id):
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner.id != current_user_id:
            return {'error': 'Action non autorisée'}, 403

        data = api.payload
        if not data:
            return {'error': 'Données manquantes'}, 400

        try:
            facade.update_place(place_id, data)
            return {'message': 'Place mise à jour avec succès'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def delete(self, place_id):
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner.id != current_user_id:
            return {'error': 'Action non autorisée'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place supprimée avec succès'}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        reviews = facade.get_reviews_by_place(place_id)
        return [{'id': r.id, 'text': r.text, 'rating': r.rating, 'user_id': r.user.id} for r in reviews], 200
