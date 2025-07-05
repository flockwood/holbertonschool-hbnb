"""Review model for our application."""
from app.models.base import BaseModel
from app import db
from sqlalchemy.orm import validates

class Review(BaseModel):
    """Represents a review of a place."""
    
    __tablename__ = 'reviews'
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), nullable=False)  # Will be foreign key later
    place_id = db.Column(db.String(36), nullable=False)  # Will be foreign key later
    
    def __init__(self, text="", rating=0, place_id="", user_id="", **kwargs):
        """Initialize a new review."""
        super().__init__(**kwargs)
        self.text = text
        self.rating = int(rating) if rating else 0
        self.place_id = place_id
        self.user_id = user_id
    
    @validates('rating')
    def validate_rating(self, key, rating):
        """Validate rating using SQLAlchemy validator."""
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            raise ValueError("Rating must be a number")
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    @validates('text')
    def validate_text(self, key, text):
        """Validate text using SQLAlchemy validator."""
        if not text or len(text.strip()) == 0:
            raise ValueError("Review text is required")
        return text.strip()
    
    @validates('user_id')
    def validate_user_id(self, key, user_id):
        """Validate user_id using SQLAlchemy validator."""
        if not user_id or len(user_id.strip()) == 0:
            raise ValueError("User ID is required")
        return user_id.strip()
    
    @validates('place_id')
    def validate_place_id(self, key, place_id):
        """Validate place_id using SQLAlchemy validator."""
        if not place_id or len(place_id.strip()) == 0:
            raise ValueError("Place ID is required")
        return place_id.strip()
    
    def validate(self):
        """Check if review data is valid (legacy method for compatibility)."""
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