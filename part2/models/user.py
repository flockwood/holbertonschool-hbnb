from app.models.base import BaseModel
import re
import bcrypt


class User(BaseModel):
    """User model representing users in the system."""
    
    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        """Initialize a User instance."""
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self._password = None
        
        # Set password if provided
        if password and not kwargs.get('_password'):
            self.password = password
        elif kwargs.get('_password'):
            self._password = kwargs.get('_password')
        
        self.places = []  # List of places owned by user
        self.reviews = []  # List of reviews written by user
        
        # Validate attributes
        self.validate()
    
    @property
    def password(self):
        """Password getter - returns None for security."""
        return None
    
    @password.setter
    def password(self, value):
        """Password setter - hashes the password before storing."""
        if value:
            self._password = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password):
        """Verify if provided password matches the stored hash."""
        if not self._password or not password:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self._password.encode('utf-8'))
    
    def validate(self):
        """Validate user attributes."""
        if not self.first_name or len(self.first_name.strip()) == 0:
            raise ValueError("First name is required")
        if len(self.first_name) > 50:
            raise ValueError("First name must not exceed 50 characters")
        
        if not self.last_name or len(self.last_name.strip()) == 0:
            raise ValueError("Last name is required")
        if len(self.last_name) > 50:
            raise ValueError("Last name must not exceed 50 characters")
        
        if not self.email or len(self.email.strip()) == 0:
            raise ValueError("Email is required")
        if not self._validate_email(self.email):
            raise ValueError("Invalid email format")
        if len(self.email) > 120:
            raise ValueError("Email must not exceed 120 characters")
        
        if not hasattr(self, '_password') or not self._password:
            raise ValueError("Password is required")
    
    def _validate_email(self, email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def to_dict(self):
        """Convert user to dictionary, excluding password."""
        data = super().to_dict()
        # Remove password from serialized data
        data.pop('_password', None)
        # Don't include related objects in serialization
        data.pop('places', None)
        data.pop('reviews', None)
        return data