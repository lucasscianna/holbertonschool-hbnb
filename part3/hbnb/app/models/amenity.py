from app.models.base_model import BaseModel
from app import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = self.validate_name(self.name)

    def validate_name(self, name):
        if not name or len(name) > 50:
            raise ValueError("Amenity name is required and must be <= 50 characters.")
        return name