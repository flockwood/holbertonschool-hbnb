"""Place model for our application."""
from app.models.base import BaseModel

class Place(BaseModel):
    """Represents a place that can be rented."""
    
    def __init__(self, title="", description="", price=0, 
                 latitude=0.0, longitude=0.0, owner_id=""):
        """Initialize a new place."""
        super().__init__()
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id
        self.amenities = []  # List of amenity IDs
        self.reviews = []    # List of review IDs
    
    def validate(self):
        """Check if place data is valid."""
        errors = []
        
        if not self.title:
            errors.append("Title is required")
        
        if not self.description:
            errors.append("Description is required")
        
        if self.price <= 0:
            errors.append("Price must be greater than 0")
        
        if not (-90 <= self.latitude <= 90):
            errors.append("Latitude must be between -90 and 90")
        
        if not (-180 <= self.longitude <= 180):
            errors.append("Longitude must be between -180 and 180")
        
        if not self.owner_id:
            errors.append("Owner ID is required")
        
        return errors
    
    def add_amenity(self, amenity_id):
        """Add an amenity to this place."""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)
    
    def remove_amenity(self, amenity_id):
        """Remove an amenity from this place."""
        if amenity_id in self.amenities:
            self.amenities.remove(amenity_id)
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenity_ids': self.amenities,
            'review_ids': self.reviews
        })
        return data