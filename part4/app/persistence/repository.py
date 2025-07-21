from abc import ABC, abstractmethod
from app import db

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Get object by attribute with case-insensitive string comparison"""
        for obj in self._storage.values():
            if hasattr(obj, attr_name):
                obj_value = getattr(obj, attr_name)
                # Case-insensitive comparison for strings
                if isinstance(obj_value, str) and isinstance(attr_value, str):
                    if obj_value.lower() == attr_value.lower():
                        return obj
                # Regular comparison for non-strings
                elif obj_value == attr_value:
                    return obj
        return None


class SQLAlchemyRepository(Repository):
    """SQLAlchemy-based repository for database persistence"""
    
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Add an object to the database"""
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Get an object by ID"""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Get all objects of this model type"""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object with new data"""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        """Delete an object by ID"""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Get object by attribute with case-insensitive string comparison for strings"""
        # For string values, do case-insensitive comparison
        if isinstance(attr_value, str):
            return self.model.query.filter(
                db.func.lower(getattr(self.model, attr_name)) == attr_value.lower()
            ).first()
        else:
            # For non-string values, do exact comparison
            return self.model.query.filter_by(**{attr_name: attr_value}).first()