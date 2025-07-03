from flask import Flask
from flask_restx import Api

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize API with configuration-aware settings
    api = Api(
        app, 
        version='1.0', 
        title='HBnB API', 
        description='HBnB Application API', 
        doc='/api/v1/'
    )

    # Register namespaces
    # User namespace
    from app.api.v1.users import api as users_ns
    api.add_namespace(users_ns, path='/api/v1/users')

    # Amenity namespace
    from app.api.v1.amenities import api as amenities_ns
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    # Places namespace
    from app.api.v1.places import api as places_ns
    api.add_namespace(places_ns, path='/api/v1/places')

    # Reviews namespace
    from app.api.v1.reviews import api as reviews_ns
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app