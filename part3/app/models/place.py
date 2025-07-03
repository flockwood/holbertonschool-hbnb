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
        self._price = 0
        self._latitude = 0
        self._longitude = 0
        self.owner_id = owner_id
        self.amenities = []  # List of amenity IDs
        self.reviews = []    # List of review IDs
        
        # Use setters for validation
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
    
    @property
    def price(self):
        """Get the price."""
        return self._price
    
    @price.setter
    def price(self, value):
        """Set the price with validation."""
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("Price must be a number")
        if value < 0:
            raise ValueError("Price must be non-negative")
        self._price = value
    
    @property
    def latitude(self):
        """Get the latitude."""
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        """Set the latitude with validation."""
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a number")
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value
    
    @property
    def longitude(self):
        """Get the longitude."""
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        """Set the longitude with validation."""
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a number")
        if not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value
    
    def validate(self):
        """Check if place data is valid."""
        errors = []
        
        if not self.title:
            errors.append("Title is required")
        
        if not self.description:
            errors.append("Description is required")
        
        if self.price <= 0:
            errors.append("Price must be greater than 0")
        
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
            'amenities': self.amenities,
            'reviews': self.reviews
        })
        return data