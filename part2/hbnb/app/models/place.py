from app.models.base_model import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __ini__(self, title, description, price, latitude, longtitude, owner):
        super().__init__()

        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longtitude = self.validate_longtitude(longtitude)
        self.owner = self.validate_owner(owner)

        self.reviews = []
        self.amenities = []
    
    def validate_title(self, title):
        if not title or len(title) > 100:
            raise ValueError("Title is required and must be <= 100 characters.")
        return title 
    
    def validate_price(self, price):
        if price <= 0:
            raise ValueError("Price must be positive.")
        return price
    
    def validate_latitude(self, lat):
        if not (-90.0 <= lat <= 90.0):
            raise ValueError("Latitude must between -90 and 90.")
        return lat
    
    def validate_longtitude(self, lon):
        if not (-180.0 <= lon <= 180.0):
            raise ValueError("Longitude must be between -180 and 180.")
        return lon
    
    def validate_owner(self, owner):
        if not isinstance(owner, User):
            raise ValueError("Owner must be a User instance.")
        return owner
    
    def add_review(self, review):
        self.reviews.append(review)
    
    def add_amenity(self, amenity):
        self.amenities.append(amenity)
()