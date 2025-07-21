"""Place model for our application with SQLAlchemy relationships."""
from app.models.base import BaseModel
from app import db
from sqlalchemy.orm import validates

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Represents a place that can be rented."""
    
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Foreign key to User
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                               backref=db.backref('places', lazy=True))
    
    def __init__(self, title="", description="", price=0, 
                 latitude=0.0, longitude=0.0, owner_id="", **kwargs):
        """Initialize a new place."""
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
    
    @validates('price')
    def validate_price(self, key, price):
        """Validate price using SQLAlchemy validator."""
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValueError("Price must be a number")
        if price < 0:
            raise ValueError("Price must be non-negative")
        return price
    
    @validates('latitude')
    def validate_latitude(self, key, latitude):
        """Validate latitude using SQLAlchemy validator."""
        try:
            latitude = float(latitude)
        except (TypeError, ValueError):
            raise ValueError("Latitude must be a number")
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return latitude
    
    @validates('longitude')
    def validate_longitude(self, key, longitude):
        """Validate longitude using SQLAlchemy validator."""
        try:
            longitude = float(longitude)
        except (TypeError, ValueError):
            raise ValueError("Longitude must be a number")
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return longitude
    
    @validates('title')
    def validate_title(self, key, title):
        """Validate title using SQLAlchemy validator."""
        if not title or len(title.strip()) == 0:
            raise ValueError("Title is required")
        return title.strip()
    
    def validate(self):
        """Check if place data is valid (legacy method for compatibility)."""
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
    
    def add_amenity(self, amenity):
        """Add an amenity to this place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
    
    def remove_amenity(self, amenity):
        """Remove an amenity from this place."""
        if amenity in self.amenities:
            self.amenities.remove(amenity)
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        })
        return data