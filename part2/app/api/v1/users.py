from flask_restx import Namespace, Resource, fields
from app.services import facade

# Create the namespace
api = Namespace('users', description='User operations')

# Define the input model for creating a user
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# Define the input model for updating a user (password optional)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='New password (optional)')
})

# Define the output model (what we return to client - NO PASSWORD!)
user_response = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})


@api.route('/')
class UserList(Resource):
    """Handle operations on user collection"""
    
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Email already registered')
    @api.marshal_with(user_response, code=201)
    def post(self):
        """Register a new user"""
        try:
            # Get data from request
            user_data = api.payload
            
            # Create user through facade
            new_user = facade.create_user(user_data)
            
            # Return user data (to_dict excludes password)
            return new_user.to_dict(), 201
            
        except ValueError as e:
            # Handle specific errors
            if "already registered" in str(e):
                api.abort(409, str(e))
            else:
                api.abort(400, str(e))
    
    @api.marshal_list_with(user_response)
    def get(self):
        """List all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    """Handle operations on a single user"""
    
    @api.response(200, 'Success')
    @api.response(404, 'User not found')
    @api.marshal_with(user_response)
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User with id {user_id} not found")
        return user.to_dict(), 200
    
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Email already registered')
    @api.marshal_with(user_response)
    def put(self, user_id):
        """Update user information"""
        try:
            user_data = api.payload
            updated_user = facade.update_user(user_id, user_data)
            return updated_user.to_dict(), 200
            
        except ValueError as e:
            if "not found" in str(e):
                api.abort(404, str(e))
            elif "already registered" in str(e):
                api.abort(409, str(e))
            else:
                api.abort(400, str(e))