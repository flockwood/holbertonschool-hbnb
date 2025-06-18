"""Base model with common attributes for all our models."""
from datetime import datetime
import uuid

class BaseModel:
    """Base class that all our models will inherit from."""
    
    def __init__(self):
        """Initialize with id and timestamps."""
        self.id = str(uuid.uuid4())  # Generate unique ID
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert object to dictionary (for JSON responses)."""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }