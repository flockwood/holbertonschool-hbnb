"""Amenity model for our application."""
from base import BaseModel

class Amenity(BaseModel):
    """Represents an amenity (like WiFi, Pool, etc.)."""
    
    def __init__(self, name=""):
        """Initialize a new amenity."""
        super().__init__()
        self.name = name
    
    def validate(self):
        """Check if amenity data is valid."""
        errors = []
        
        if not self.name:
            errors.append("Amenity name is required")
        
        return errors
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data['name'] = self.name
        return data