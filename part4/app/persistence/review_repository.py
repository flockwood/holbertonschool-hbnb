"""Review-specific repository for database operations."""
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app import db

class ReviewRepository(SQLAlchemyRepository):
    """Repository for Review entity with specific review operations."""
    
    def __init__(self):
        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place."""
        return self.model.query.filter_by(place_id=place_id).all()
    
    def get_reviews_by_user(self, user_id):
        """Get all reviews written by a specific user."""
        return self.model.query.filter_by(user_id=user_id).all()
    
    def get_reviews_by_rating(self, rating):
        """Get all reviews with a specific rating."""
        return self.model.query.filter_by(rating=rating).all()
    
    def get_reviews_by_rating_range(self, min_rating=None, max_rating=None):
        """Get reviews within a specific rating range."""
        query = self.model.query
        
        if min_rating is not None:
            query = query.filter(self.model.rating >= min_rating)
        if max_rating is not None:
            query = query.filter(self.model.rating <= max_rating)
            
        return query.all()
    
    def get_average_rating_for_place(self, place_id):
        """Calculate average rating for a specific place."""
        result = db.session.query(db.func.avg(self.model.rating)).filter_by(place_id=place_id).scalar()
        return float(result) if result else 0.0
    
    def count_reviews_for_place(self, place_id):
        """Count total reviews for a specific place."""
        return self.model.query.filter_by(place_id=place_id).count()
    
    def user_has_reviewed_place(self, user_id, place_id):
        """Check if a user has already reviewed a specific place."""
        return self.model.query.filter_by(user_id=user_id, place_id=place_id).first() is not None