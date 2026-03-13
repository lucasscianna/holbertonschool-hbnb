from app.models.base_model import BaseModel
from app.models.user import User
from app import db

class Place(BaseModel):
    __tablename__= 'places'
    """Représente un logement disponible à la location."""

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, **kwargs):
        """Initialise un logement avec ses coordonnées et son propriétaire."""
        owner = kwargs.get('owner')

        super().__init__(**kwargs)

        self.validate_title(self.title)
        self.validate_price(self.price)
        self.validate_latitude(self.latitude)
        self.validate_longitude(self.longitude)

        self.owner = self.validate_owner(owner) if owner else None
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
