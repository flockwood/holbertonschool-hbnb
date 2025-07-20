"""Place-specific repository for database operations."""
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place entity with specific place operations."""
    
    def __init__(self):
        super().__init__(Place)

    def get_places_by_owner(self, owner_id):
        """Get all places owned by a specific user."""
        return self.model.query.filter_by(owner_id=owner_id).all()
    
    def get_places_by_price_range(self, min_price=None, max_price=None):
        """Get places within a specific price range."""
        query = self.model.query
        
        if min_price is not None:
            query = query.filter(self.model.price >= min_price)
        if max_price is not None:
            query = query.filter(self.model.price <= max_price)
            
        return query.all()
    
    def get_places_by_location(self, latitude, longitude, radius=1.0):
        """Get places within a radius of given coordinates (simple implementation)."""
        # Simple bounding box search (for production, use spatial databases)
        lat_min = latitude - radius
        lat_max = latitude + radius
        lng_min = longitude - radius
        lng_max = longitude + radius
        
        return self.model.query.filter(
            self.model.latitude.between(lat_min, lat_max),
            self.model.longitude.between(lng_min, lng_max)
        ).all()
    
    def count_places(self):
        """Count total number of places."""
        return self.model.query.count()
    
    def get_places_by_title(self, title_part):
        """Search places by title (case-insensitive partial match)."""
        return self.model.query.filter(
            self.model.title.ilike(f'%{title_part}%')
        ).all()