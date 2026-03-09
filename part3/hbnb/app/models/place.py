from app.models.base_model import BaseModel
from app.models.user import User

class Place(BaseModel):
    """Représente un logement disponible à la location."""

    def __init__(self, title, description, price, latitude, longitude, owner):
        """Initialise un logement avec ses coordonnées et son propriétaire."""
        super().__init__()
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = self.validate_owner(owner)
        self.reviews = []
        self.amenities = []

    def validate_title(self, title):
        """Valide que le titre n'est pas vide et ne dépasse pas 100 caractères."""
        if not title or len(title) > 100:
            raise ValueError("Le titre est requis (max 100 caractères).")
        return title 

    def validate_price(self, price):
        """Vérifie que le prix est un nombre positif."""
        if price <= 0:
            raise ValueError("Le prix doit être positif.")
        return price

    def validate_latitude(self, lat):
        """Vérifie que la latitude est comprise entre -90 et 90."""
        if not (-90.0 <= lat <= 90.0):
            raise ValueError("La latitude doit être entre -90 et 90.")
        return lat

    def validate_longitude(self, lon):
        """Vérifie que la longitude est comprise entre -180 et 180."""
        if not (-180.0 <= lon <= 180.0):
            raise ValueError("La longitude doit être entre -180 et 180.")
        return lon

    def validate_owner(self, owner):
        """Vérifie que le propriétaire est bien une instance de la classe User."""
        if not isinstance(owner, User):
            raise ValueError("Le propriétaire doit être une instance de User.")
        return owner

    def add_review(self, review):
        """Ajoute un avis à la liste des avis du logement."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Ajoute un équipement à la liste des équipements du logement."""
        self.amenities.append(amenity)
