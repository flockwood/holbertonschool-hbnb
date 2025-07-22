from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        # Using SQLAlchemy repositories for all entities
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # --- User methods ---
    def create_user(self, user_data):
        """Create a new user"""
        # Check if email already exists using the UserRepository method
        existing_user = self.user_repo.get_user_by_email(user_data.get('email'))
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create user instance
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            password=user_data.get('password')
        )
        
        # Validate user data (legacy validation for compatibility)
        errors = user.validate()
        if errors:
            raise ValueError(", ".join(errors))
        
        # Save to repository (will commit to database)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get user by email"""
        return self.user_repo.get_user_by_email(email)
    
    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        """Update user information"""
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        # Check if email is being changed to an existing email
        new_email = user_data.get('email')
        if new_email and new_email != user.email:
            existing_user = self.get_user_by_email(new_email)
            if existing_user:
                raise ValueError("Email already registered")
        
        # Update the user attributes
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']
        if 'password' in user_data:
            user.hash_password(user_data['password'])
        if 'is_admin' in user_data:
            user.is_admin = user_data['is_admin']
        
        # Validate after update
        errors = user.validate()
        if errors:
            raise ValueError(", ".join(errors))
        
        # Save changes to database
        user.save()
        
        return user

    def make_user_admin(self, user_id):
        """Make a user an admin (for testing purposes)"""
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        user.is_admin = True
        user.save()
        return user

    # --- Amenity methods (now using SQLAlchemy) ---
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        # Check if amenity with same name already exists
        existing_amenity = self.amenity_repo.get_amenity_by_name(amenity_data.get('name'))
        if existing_amenity:
            raise ValueError(f"Amenity with name '{amenity_data.get('name')}' already exists")
        
        # Create amenity instance
        amenity = Amenity(name=amenity_data.get('name'))
        
        # Validate amenity data
        errors = amenity.validate()
        if errors:
            raise ValueError(", ".join(errors))
        
        # Save to repository (will commit to database)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        """Get amenity by name"""
        return self.amenity_repo.get_amenity_by_name(name)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity information"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError(f"Amenity with id {amenity_id} not found")
        
        # Check if new name already exists (if name is being changed)
        new_name = amenity_data.get('name')
        if new_name and new_name != amenity.name:
            existing_amenity = self.get_amenity_by_name(new_name)
            if existing_amenity:
                raise ValueError(f"Amenity with name '{new_name}' already exists")
        
        # Update the amenity attributes
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        
        # Validate after update
        errors = amenity.validate()
        if errors:
            raise ValueError(", ".join(errors))
        
        # Save changes to database
        amenity.save()
        
        return amenity
    
    # --- Place methods (now using SQLAlchemy relationships) ---
    def create_place(self, place_data):
        """Create a new place"""
        # Check owner exists (using UserRepository)
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            raise ValueError(f"Owner with id {place_data.get('owner_id')} not found")
        
        # Create place
        place = Place(
            title=place_data.get('title', ''),
            description=place_data.get('description', ''),
            price=place_data.get('price', 0),
            latitude=place_data.get('latitude', 0),
            longitude=place_data.get('longitude', 0),
            owner_id=place_data.get('owner_id')
        )
        
        # Handle amenities (many-to-many relationship)
        amenity_ids = place_data.get('amenities', [])
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with id {amenity_id} not found")
            place.add_amenity(amenity)
        
        # Validate and save
        errors = place.validate()
        if errors:
            raise ValueError(", ".join(errors))
        
        # Save to repository (will commit to database)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get place details with relationships"""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        # Create detailed response using relationships
        result = place.to_dict()
        
        # Add owner info using relationship
        if place.owner:
            result['owner'] = place.owner.to_dict()
        
        # Add amenities info using relationship
        result['amenities'] = [amenity.to_dict() for amenity in place.amenities]
        
        return result

    def get_all_places(self):
        """Get all places with basic info including price"""
        places = self.place_repo.get_all()
        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'price': place.price  # ADDED PRICE HERE
        } for place in places]

    def update_place(self, place_id, place_data):
        """Update place using relationships"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with id {place_id} not found")
        
        # Update basic fields
        for field in ['title', 'description', 'price', 'latitude', 'longitude']:
            if field in place_data:
                setattr(place, field, place_data[field])
        
        # Update owner if provided
        if 'owner_id' in place_data:
            new_owner = self.get_user(place_data['owner_id'])
            if not new_owner:
                raise ValueError(f"Owner with id {place_data['owner_id']} not found")
            place.owner_id = place_data['owner_id']
        
        # Update amenities if provided (many-to-many)
        if 'amenities' in place_data:
            # Clear existing amenities
            place.amenities.clear()
            # Add new amenities
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with id {amenity_id} not found")
                place.add_amenity(amenity)
        
        # Validate and save
        errors = place.validate()
        if errors:
            raise ValueError(", ".join(errors))
        
        # Save changes to database
        place.save()
        
        return place

    # --- Review methods (now using SQLAlchemy relationships) ---
    def create_review(self, review_data):
        """Create a new review using relationships"""
        # Check user and place exist
        user = self.get_user(review_data.get('user_id'))
        if not user:
            raise ValueError(f"User with id {review_data.get('user_id')} not found")
        
        place = self.place_repo.get(review_data.get('place_id'))
        if not place:
            raise ValueError(f"Place with id {review_data.get('place_id')} not found")
        
        # Create and validate review
        review = Review(
            text=review_data.get('text', ''),
            rating=review_data.get('rating', 0),
            place_id=review_data.get('place_id'),
            user_id=review_data.get('user_id')
        )
        
        errors = review.validate()
        if errors:
            raise ValueError(", ".join(errors))
        
        # Save to repository (will commit to database)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get reviews for a place using relationships"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with id {place_id} not found")
        
        # Use relationship to get reviews
        return place.reviews

    def update_review(self, review_id, review_data):
        """Update review"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with id {review_id} not found")
        
        # Update provided fields
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']
        
        errors = review.validate()
        if errors:
            raise ValueError(", ".join(errors))
        
        # Save changes to database
        review.save()
        
        return review

    def delete_review(self, review_id):
        """Delete review"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with id {review_id} not found")
        
        # Delete from repository (will commit to database)
        self.review_repo.delete(review_id)
        return True

    # --- Additional relationship methods ---
    def get_user_places(self, user_id):
        """Get all places owned by a user using relationships"""
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        return user.places

    def get_user_reviews(self, user_id):
        """Get all reviews written by a user using relationships"""
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        return user.reviews

    def get_place_reviews(self, place_id):
        """Get all reviews for a place using relationships"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with id {place_id} not found")
        
        return place.reviews

    def get_amenity_places(self, amenity_id):
        """Get all places that have a specific amenity"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError(f"Amenity with id {amenity_id} not found")
        
        return amenity.places