"""Amenity model for our application."""
from app.models.base import BaseModel
from app import db
from sqlalchemy.orm import validates

class Amenity(BaseModel):
    """Represents an amenity (like WiFi, Pool, etc.)."""
    
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    def __init__(self, name="", **kwargs):
        """Initialize a new amenity."""
        super().__init__(**kwargs)
        self.name = name
    
    @validates('name')
    def validate_name(self, key, name):
        """Validate name using SQLAlchemy validator."""
        if not name or len(name.strip()) == 0:
            raise ValueError("Amenity name is required")
        return name.strip()
    
    def validate(self):
        """Check if amenity data is valid (legacy method for compatibility)."""
        errors = []
        
        if not self.name:
            errors.append("Amenity name is required")
        
        return errors
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data['name'] = self.name
        return data