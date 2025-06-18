from flask_restx import Namespace, Resource, fields
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
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Amenity already exists')
    @api.marshal_with(amenity_response, code=201)
    def post(self):
        """Register a new amenity"""
        try:
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
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @api.marshal_with(amenity_response)
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity with id {amenity_id} not found")
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Amenity name already exists')
    @api.marshal_with(amenity_response)
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
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