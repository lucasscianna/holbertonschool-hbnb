import re
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel
from app import db, bcrypt

class User(BaseModel):
    """Represents a user in the system."""
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        """Ensures the name is not empty and does not exceed 50 characters."""
        if not value or len(value) > 50:
            field_name = "First name" if key == "first_name" else "Last name"
            raise ValueError(f"{field_name} is required (max 50 characters).")
        return value
    
    @validates('email')
    def validate_email(self, key, email):
        """Validates the email format and ensures its uniqueness."""
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")
        return email

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the stored hashed password."""
        return bcrypt.check_password_hash(self.password, password)