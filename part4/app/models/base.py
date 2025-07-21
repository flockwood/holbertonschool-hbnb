"""Base model with common attributes for all our models."""
from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    """Base class that all our models will inherit from."""
    
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert object to dictionary (for JSON responses)."""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }