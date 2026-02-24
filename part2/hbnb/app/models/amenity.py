from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self.validate_name(name)

        def validate_name(self, name):
            if not name or len(name) > 50:
                raise ValueError("Amenity name is required and must be <= 50 characters.")
            return name