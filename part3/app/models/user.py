"""User model for our application."""
from app.models.base import BaseModel
import re

class User(BaseModel):
    """Represents a user in our system."""
    
    def __init__(self, first_name="", last_name="", email="", password=""):
        """Initialize a new user."""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = False
        
        # Hash the password if provided
        if password:
            self.hash_password(password)
        else:
            self.password = None
    
    def hash_password(self, password):
        """Hashes the password before storing it."""
        # Import bcrypt here to avoid circular imports
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        if not self.password:
            return False
        # Import bcrypt here to avoid circular imports
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)
    
    def validate(self):
        """Check if user data is valid."""
        errors = []
        
        # Check first name
        if not self.first_name or len(self.first_name.strip()) == 0:
            errors.append("First name is required")
        
        # Check last name
        if not self.last_name or len(self.last_name.strip()) == 0:
            errors.append("Last name is required")
        
        # Check email
        if not self.email:
            errors.append("Email is required")
        elif not self._is_valid_email(self.email):
            errors.append("Invalid email format")
        
        # Check password
        if not self.password:
            errors.append("Password is required")
        
        return errors
    
    def _is_valid_email(self, email):
        """Check if email format is valid."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    def to_dict(self):
        """Convert to dictionary, excluding password."""
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        # Never include password in response!
        return data