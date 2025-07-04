from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Define the output model
amenity_response = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(409, 'Amenity already exists')
    @api.marshal_with(amenity_response, code=201)
    def post(self):
        """Create a new amenity (Admin only)"""
        try:
            # Check if user is admin
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            if not is_admin:
                api.abort(403, 'Admin privileges required')
            
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
            
        except ValueError as e:
            if "already exists" in str(e):
                api.abort(409, str(e))
            else:
                api.abort(400, str(e))

    @api.response(200, 'List of amenities retrieved successfully')
    @api.marshal_list_with(amenity_response)
    def get(self):
        """Retrieve a list of all amenities (Public access)"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @api.marshal_with(amenity_response)
    def get(self, amenity_id):
        """Get amenity details by ID (Public access)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity with id {amenity_id} not found")
        return amenity.to_dict(), 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(409, 'Amenity name already exists')
    @api.marshal_with(amenity_response)
    def put(self, amenity_id):
        """Update an amenity's information (Admin only)"""
        try:
            # Check if user is admin
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            if not is_admin:
                api.abort(403, 'Admin privileges required')
            
            amenity_data = api.payload
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return updated_amenity.to_dict(), 200
            
        except ValueError as e:
            if "not found" in str(e):
                api.abort(404, str(e))
            elif "already exists" in str(e):
                api.abort(409, str(e))
            else:
                api.abort(400, str(e))