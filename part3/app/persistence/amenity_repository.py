"""Amenity-specific repository for database operations."""
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository
from app import db

class AmenityRepository(SQLAlchemyRepository):
    """Repository for Amenity entity with specific amenity operations."""
    
    def __init__(self):
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        """Get an amenity by name (case-insensitive)."""
        if not name:
            return None
        return self.model.query.filter(
            db.func.lower(self.model.name) == name.lower()
        ).first()
    
    def get_amenities_by_name_pattern(self, pattern):
        """Get amenities that match a name pattern (case-insensitive)."""
        return self.model.query.filter(
            self.model.name.ilike(f'%{pattern}%')
        ).all()
    
    def count_amenities(self):
        """Count total number of amenities."""
        return self.model.query.count()
    
    def amenity_exists(self, name):
        """Check if an amenity with given name exists."""
        return self.get_amenity_by_name(name) is not None