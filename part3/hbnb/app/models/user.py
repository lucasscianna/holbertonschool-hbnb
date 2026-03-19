import re
from app import db, bcrypt
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email      = db.Column(db.String(120), nullable=False, unique=True)
    password   = db.Column(db.String(128), nullable=False)
    is_admin   = db.Column(db.Boolean, default=False)

    # ── Relations ajoutées T8 ──
    places  = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    @validates('first_name')
    def validate_first_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("First name est requis (max 50 caractères).")
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("Last name est requis (max 50 caractères).")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not value or not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise ValueError("Format d'email invalide.")
        return value

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)