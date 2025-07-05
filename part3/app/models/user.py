"""User model for our application with SQLAlchemy relationships."""
from app.models.base import BaseModel
from app import db
import re
from sqlalchemy.orm import validates

class User(BaseModel):
    """Represents a user in our system."""
    
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, first_name="", last_name="", email="", password="", **kwargs):
        """Initialize a new user."""
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = False
        
        # Hash the password if provided
        if password:
            self.hash_password(password)
    
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
    
    @validates('email')
    def validate_email(self, key, email):
        """Validate email format using SQLAlchemy validator."""
        if not email:
            raise ValueError("Email is required")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        return email
    
    @validates('first_name')
    def validate_first_name(self, key, first_name):
        """Validate first name using SQLAlchemy validator."""
        if not first_name or len(first_name.strip()) == 0:
            raise ValueError("First name is required")
        return first_name.strip()
    
    @validates('last_name')
    def validate_last_name(self, key, last_name):
        """Validate last name using SQLAlchemy validator."""
        if not last_name or len(last_name.strip()) == 0:
            raise ValueError("Last name is required")
        return last_name.strip()
    
    def validate(self):
        """Check if user data is valid (legacy method for compatibility)."""
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