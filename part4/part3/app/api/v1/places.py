from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

# Output model for place list (PUBLIC - no authentication needed)
place_list_model = api.model('PlaceList', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude')
})

# Output model for detailed place (PUBLIC - no authentication needed)
place_detail_model = api.model('PlaceDetail', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(user_model),
    'amenities': fields.List(fields.Nested(amenity_model)),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    def post(self):
        """Create a new place (Authentication required)"""
        try:
            # Get current authenticated user
            current_user = get_jwt_identity()
            
            place_data = api.payload.copy()
            # Set owner_id to current authenticated user
            place_data['owner_id'] = current_user
            
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
            
        except ValueError as e:
            if "not found" in str(e):
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))

    @api.response(200, 'List of places retrieved successfully')
    @api.marshal_list_with(place_list_model)
    def get(self):
        """Retrieve a list of all places (Public access)"""
        places = facade.get_all_places()
        return places, 200

@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (Public access)"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place with id {place_id} not found")
        return place, 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information (Authentication required - Owner or Admin)"""
        try:
            # Get current authenticated user and claims
            current_user = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Get the place to check ownership
            place = facade.get_place(place_id)
            if not place:
                api.abort(404, f"Place with id {place_id} not found")
            
            # Check if current user owns the place OR is an admin
            if not is_admin and place.get('owner', {}).get('id') != current_user:
                api.abort(403, 'Unauthorized action')
            
            place_data = api.payload
            updated_place = facade.update_place(place_id, place_data)
            return {'message': 'Place updated successfully'}, 200
            
        except ValueError as e:
            if "not found" in str(e):
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))