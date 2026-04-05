import re
from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        if not user_data.get("first_name") or not user_data.get("last_name"):
            raise ValueError("First and last name are required")
        email = user_data.get("email")
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        if self.get_user_by_email(email):
            raise ValueError("Email already registered")

        all_users = self.user_repo.get_all()
        is_admin = (len(all_users) == 0)

        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=is_admin
        )
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            if key == "password":
                user.hash_password(value)
            elif hasattr(user, key):
                setattr(user, key, value)
        from app import db
        db.session.commit()
        return user

    def create_place(self, place_data):
        owner = self.get_user(place_data.get("owner_id"))
        if not owner: raise ValueError("Owner not found")
        if not place_data.get("title"): raise ValueError("Title is required")
        price = place_data.get("price")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number")
        lat = place_data.get("latitude")
        lon = place_data.get("longitude")
        if not isinstance(lat, (int, float)) or not (-90 <= lat <= 90):
            raise ValueError("Invalid latitude")
        if not isinstance(lon, (int, float)) or not (-180 <= lon <= 180):
            raise ValueError("Invalid longitude")
        if not place_data.get("country"):
            raise ValueError("Country is required")
        place = Place(title=place_data["title"], description=place_data.get("description"),
                      price=price, latitude=lat, longitude=lon, owner=owner, country=place_data["country"])
        for aid in place_data.get('amenities', []):
            amenity = self.get_amenity(aid)
            if amenity: place.add_amenity(amenity)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place: return None
        for key in ['title', 'description', 'price', 'latitude', 'longitude', 'country']:
            if key in place_data: setattr(place, key, place_data[key])
        return place

    def delete_place(self, place_id):
        self.place_repo.delete(place_id)

    def create_review(self, review_data):
        if not review_data.get("text"): raise ValueError("Review text is required")
        rating = review_data.get("rating")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        user = self.get_user(review_data.get("user_id"))
        place = self.get_place(review_data.get("place_id"))
        if not user or not place: raise ValueError("User or Place not found")
        review = Review(text=review_data["text"], rating=rating, user=user, place=place)
        self.review_repo.add(review)
        if review not in place.reviews:
            place.reviews.append(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        return place.reviews if place else []

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review: return None
        if "text" in review_data:
            if not review_data["text"]: raise ValueError("Text cannot be empty")
            review.text = review_data["text"]
        if "rating" in review_data:
            rating = review_data["rating"]
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("Invalid rating")
            review.rating = rating
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review: return False
        if review.place and review in review.place.reviews:
            review.place.reviews.remove(review)
        self.review_repo.delete(review_id)
        return True

    def create_amenity(self, amenity_data):
        if not amenity_data.get("name"): raise ValueError("Name required")
        amenity = Amenity(name=amenity_data["name"])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity: return None
        if "name" in amenity_data: amenity.name = amenity_data["name"]
        return amenity