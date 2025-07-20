from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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

# Define the input model for updating a user (restricted fields for regular users)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user')
})

# Define the admin update model (includes all fields)
admin_user_update_model = api.model('AdminUserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password of the user'),
    'is_admin': fields.Boolean(description='Admin status')
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
    
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(409, 'Email already registered')
    @api.marshal_with(user_response, code=201)
    def post(self):
        """Create a new user (Admin only)"""
        try:
            # Check if user is admin
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            if not is_admin:
                api.abort(403, 'Admin privileges required')
            
            user_data = api.payload
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
            
        except ValueError as e:
            if "already registered" in str(e):
                api.abort(409, str(e))
            else:
                api.abort(400, str(e))
    
    @api.marshal_list_with(user_response)
    def get(self):
        """List all users (Public access)"""
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
        """Get user details by ID (Public access)"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User with id {user_id} not found")
        return user.to_dict(), 200
    
    @jwt_required()
    @api.response(200, 'User successfully updated')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(user_response)
    def put(self, user_id):
        """Update user information (Authentication required)"""
        try:
            # Get current authenticated user and claims
            current_user = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Check authorization
            if not is_admin and user_id != current_user:
                api.abort(403, 'Unauthorized action')
            
            # Determine which fields are allowed based on role
            if is_admin:
                # Admin can modify any field
                user_data = api.payload
            else:
                # Regular user can only modify first_name and last_name
                allowed_fields = ['first_name', 'last_name']
                # Check if user is trying to modify restricted fields
                restricted_fields = set(api.payload.keys()) - set(allowed_fields)
                if restricted_fields:
                    api.abort(400, 'You cannot modify email or password')
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