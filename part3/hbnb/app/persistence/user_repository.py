from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        """Initialize the repository with the User model."""
        super().__init__(User)
    
    def get_user_by_email(self, email):
        """Search a user with his email (specify to User)."""
        return self.model.query.filter_by(email=email).first()