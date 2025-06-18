from datetime import datetime
import uuid
from typing import Any, Dict


class BaseModel:
    """Base class for all models with common attributes and methods."""
    
    def __init__(self, **kwargs):
        """Initialize base model with id and timestamps."""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.fromisoformat(value) if isinstance(value, str) else value
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
    
    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()
    
    def update(self, data: Dict[str, Any]):
        """Update model attributes from dictionary."""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.save()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary representation."""
        data = self.__dict__.copy()
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data['__class__'] = self.__class__.__name__
        return data
