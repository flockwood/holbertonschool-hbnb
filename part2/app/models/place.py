from app.models.base import BaseModel
from typing import List, Optional


class Place(BaseModel):
    """Place model representing properties in the system."""
    
    def __init__(self, title, description, price, latitude, longitude, owner, **kwargs):
        """Initialize a Place instance."""
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List of reviews for this place
        self.amenities = []  # List of amenities available at this place
        
        # Add this place to owner's places list
        if hasattr(owner, 'places') and self not in owner.places:
            owner.places.append(self)
        
        # Validate attributes
        self.validate()
    
    def validate(self):
        """Validate place attributes."""
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Title is required")
        if len(self.title) > 100:
            raise ValueError("Title must not exceed 100 characters")
        
        if not self.description:
            raise ValueError("Description is required")
        
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            raise ValueError("Price must be a positive number")
        
        if not isinstance(self.latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if self.latitude < -90 or self.latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")
        
        if not isinstance(self.longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        if self.longitude < -180 or self.longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")
        
        if not self.owner:
            raise ValueError("Owner is required")
    
    def add_amenity(self, amenity):
        """Add an amenity to this place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            if hasattr(amenity, 'places') and self not in amenity.places:
                amenity.places.append(self)
    
    def remove_amenity(self, amenity):
        """Remove an amenity from this place."""
        if amenity in self.amenities:
            self.amenities.remove(amenity)
            if hasattr(amenity, 'places') and self in amenity.places:
                amenity.places.remove(self)
    
    def add_review(self, review):
        """Add a review to this place."""
        if review not in self.reviews:
            self.reviews.append(review)
    
    def get_average_rating(self) -> Optional[float]:
        """Calculate and return the average rating of all reviews."""
        if not self.reviews:
            return None
        total_rating = sum(review.rating for review in self.reviews)
        return round(total_rating / len(self.reviews), 2)
    
    def to_dict(self):
        """Convert place to dictionary."""
        data = super().to_dict()
        # Include owner id instead of object
        data['owner_id'] = self.owner.id if self.owner else None
        # Include amenity ids
        data['amenity_ids'] = [amenity.id for amenity in self.amenities]
        # Include average rating
        data['average_rating'] = self.get_average_rating()
        # Don't include full objects
        data.pop('owner', None)
        data.pop('reviews', None)
        data.pop('amenities', None)
        return data