from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Create extension instances
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Initialize API
    api = Api(
        app, 
        version='1.0', 
        title='HBnB API', 
        description='HBnB Application API', 
        doc='/api/v1/'
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

    # Create admin user on startup (for development/testing)
    @app.before_first_request
    def create_admin_user():
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
                print("✅ Admin user created automatically on startup")
                print("   Email: admin@hbnb.com")
                print("   Password: admin123")
            else:
                # Ensure existing user is admin
                if not admin.is_admin:
                    admin.is_admin = True
                    print("✅ Existing admin user privileges confirmed")
        except Exception as e:
            print(f"⚠️  Admin user creation failed: {e}")
            print("   You may need to create an admin user manually")

    return app