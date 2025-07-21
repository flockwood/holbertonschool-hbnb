"""User-specific repository for database operations."""
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    """Repository for User entity with specific user operations."""
    
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Get a user by email address."""
        if not email:
            return None
        return self.model.query.filter_by(email=email).first()
    
    def get_all_admins(self):
        """Get all users with admin privileges."""
        return self.model.query.filter_by(is_admin=True).all()
    
    def get_users_by_name(self, first_name=None, last_name=None):
        """Get users by first name and/or last name."""
        query = self.model.query
        
        if first_name:
            query = query.filter(self.model.first_name.ilike(f'%{first_name}%'))
        if last_name:
            query = query.filter(self.model.last_name.ilike(f'%{last_name}%'))
            
        return query.all()
    
    def count_users(self):
        """Count total number of users."""
        return self.model.query.count()
    
    def user_exists(self, email):
        """Check if a user with given email exists."""
        return self.model.query.filter_by(email=email).first() is not None