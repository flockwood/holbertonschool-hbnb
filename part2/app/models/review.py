"""Review model for our application."""
from base import BaseModel

class Review(BaseModel):
    """Represents a review of a place."""
    
    def __init__(self, text="", rating=0, place_id="", user_id=""):
        """Initialize a new review."""
        super().__init__()
        self.text = text
        self.rating = int(rating)
        self.place_id = place_id
        self.user_id = user_id
    
    def validate(self):
        """Check if review data is valid."""
        errors = []
        
        if not self.text:
            errors.append("Review text is required")
        
        if not (1 <= self.rating <= 5):
            errors.append("Rating must be between 1 and 5")
        
        if not self.place_id:
            errors.append("Place ID is required")
        
        if not self.user_id:
            errors.append("User ID is required")
        
        return errors
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id
        })
        return data