from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    def __init__(self, **kwargs):
        place = kwargs.pop('place', None)
        user = kwargs.pop('user', None)

        super().__init__(**kwargs)

        self.validate_texte(self.text)
        self.validate_rating(self.rating)

        self.place = self.validate_place(place) if place else None
        self.user = self.validate_user(user) if user else None

        if self.place and hasattr(self.place, 'add_review'):
            self.place.add_review(self)

    def validate_texte(self, text):
        if not text:
            raise ValueError("Review text is requiered.")
        return text
    
    def validate_rating(self, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return rating
    
    def validate_place(self, place):
        if not isinstance(place, Place):
            raise ValueError("Place must be a Place instance.")
        return place
    
    def validate_user(self, user):
        if not isinstance(user, User):
            raise ValueError("User must be a User instance.")
        return user
