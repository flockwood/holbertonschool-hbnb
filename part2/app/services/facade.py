from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- User methods ---
    def create_user(self, user_data):
        """Create a new user"""
        # Check if email already exists
        existing_user = self.get_user_by_email(user_data.get('email'))
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create user instance
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            password=user_data.get('password')  # Your model handles hashing
        )
        
        # Validate user data
        errors = user.validate()
        if errors:
            raise ValueError(", ".join(errors))
        
        # Save to repository
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get user by email"""
        return self.user_repo.get_by_attribute('email', email)
    
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
            user.password_hash = user._hash_password(user_data['password'])
        
        # Validate after update
        errors = user.validate()
        if errors:
            raise ValueError(", ".join(errors))
        
        # Update timestamp (if BaseModel has this method)
        if hasattr(user, 'save'):
            user.save()  # This should update the updated_at timestamp
        
        return user
     # --- Amenity methods ---
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        # Check if amenity with same name already exists
        existing_amenity = self.get_amenity_by_name(amenity_data.get('name'))
        if existing_amenity:
            raise ValueError(f"Amenity with name '{amenity_data.get('name')}' already exists")
        
        # Create amenity instance
        amenity = Amenity(name=amenity_data.get('name'))
        
        # Validate amenity data
        errors = amenity.validate()
        if errors:
            raise ValueError(", ".join(errors))
        
        # Save to repository
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        """Get amenity by name"""
        if not name:
            return None
        # Make case-insensitive comparison
        return self.amenity_repo.get_by_attribute('name', name.strip())

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
        
        # Update timestamp
        if hasattr(amenity, 'save'):
            amenity.save()
        
        return amenity