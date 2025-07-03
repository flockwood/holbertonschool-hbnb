from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with user ID as identity and additional claims
        access_token = create_access_token(
            identity=str(user.id),  # Use string for identity
            additional_claims={'is_admin': user.is_admin}  # Add claims separately
        )
        
        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @api.response(200, 'Access granted')
    @api.response(401, 'Invalid or missing token')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        from flask_jwt_extended import get_jwt_claims, get_jwt
        
        # Get user ID from token identity
        current_user_id = get_jwt_identity()
        
        # Get additional claims (like is_admin)
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        return {
            'message': f'Hello, user {current_user_id}',
            'user_id': current_user_id,
            'is_admin': is_admin
        }, 200