from flask import Flask, send_from_directory
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Create extension instances
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    CORS(app)  # Enable CORS for frontend-backend communication
    
    # Serve frontend files
    @app.route('/')
    def index():
        return send_from_directory('../frontend', 'index.html')
    
    @app.route('/<path:filename>')
    def serve_static(filename):
        # Don't serve API routes as static files
        if filename.startswith('api/'):
            return "Not Found", 404
        return send_from_directory('../frontend', filename)
    
    # Initialize API with updated doc path to avoid conflicts
    api = Api(
        app, 
        version='1.0', 
        title='HBnB API', 
        description='HBnB Application API', 
        doc='/api/v1/doc/'  # Changed from '/api/v1/' to avoid conflict with static files
    )

    # Register namespaces
    from app.api.v1.users import api as users_ns
    api.add_namespace(users_ns, path='/api/v1/users')

    from app.api.v1.amenities import api as amenities_ns
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    from app.api.v1.places import api as places_ns
    api.add_namespace(places_ns, path='/api/v1/places')

    from app.api.v1.reviews import api as reviews_ns
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    # Register auth namespace
    from app.api.v1.auth import api as auth_ns
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Initialize database and create admin user
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        try:
            from app.services import facade
            
            # Check if admin user already exists
            admin = facade.get_user_by_email('admin@hbnb.com')
            if not admin:
                admin_data = {
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'email': 'admin@hbnb.com',
                    'password': 'admin123'
                }
                admin = facade.create_user(admin_data)
                admin.is_admin = True
                admin.save()  # Save to database
                print("✅ Admin user created automatically on startup")
                print("   Email: admin@hbnb.com")
                print("   Password: admin123")
            else:
                # Ensure existing user is admin
                if not admin.is_admin:
                    admin.is_admin = True
                    admin.save()
                print("✅ Admin user ready")
                print("   Email: admin@hbnb.com") 
                print("   Password: admin123")
        except Exception as e:
            print(f"⚠️  Admin user creation failed: {e}")

    return app