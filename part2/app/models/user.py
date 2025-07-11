"""User model for our application."""
from app.models.base import BaseModel
import bcrypt
import re

class User(BaseModel):
    """Represents a user in our system."""
    
    def __init__(self, first_name="", last_name="", email="", password=""):
        """Initialize a new user."""
        super().__init__()  # Call parent class constructor
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = False  # Regular user by default
        
        # Hash the password for security
        if password:
            self.password_hash = self._hash_password(password)
        else:
            self.password_hash = None
    
    def _hash_password(self, password):
        """Hash a password for storing."""
        # Convert password to bytes and hash it
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password):
        """Check if provided password is correct."""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            self.password_hash.encode('utf-8')
        )
    
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
        if not self.password_hash:
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