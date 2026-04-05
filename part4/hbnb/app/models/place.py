from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates

# ── Table d'association Many-to-Many Place <-> Amenity ──
place_amenity = db.Table('place_amenity',
    db.Column('place_id',   db.String(36), db.ForeignKey('places.id'),    primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    price       = db.Column(db.Float, nullable=False)
    latitude    = db.Column(db.Float, nullable=False)
    longitude   = db.Column(db.Float, nullable=False)
    country     = db.Column(db.String(100), nullable=False)

    # ── Relations ajoutées T8 ──
    owner_id  = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    reviews   = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                                backref=db.backref('places', lazy=True))

    def __init__(self, title, description, price, latitude, longitude, owner, country):
        super().__init__()
        self.title       = title
        self.description = description
        self.price       = price
        self.latitude    = latitude
        self.longitude   = longitude
        self.owner_id    = owner.id
        self.owner       = owner
        self.country     = country

    @validates('title')
    def validate_title(self, key, value):
        if not value or len(value) > 100:
            raise ValueError("Le titre est requis (max 100 caractères).")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("Le prix doit être positif.")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not (-90.0 <= value <= 90.0):
            raise ValueError("La latitude doit être entre -90 et 90.")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not (-180.0 <= value <= 180.0):
            raise ValueError("La longitude doit être entre -180 et 180.")
        return value

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)