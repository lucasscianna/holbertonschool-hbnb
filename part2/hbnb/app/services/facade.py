from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email')
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()
