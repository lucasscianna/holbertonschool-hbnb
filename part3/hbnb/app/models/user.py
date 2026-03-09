import re
from app.models.base_model import BaseModel
from app import bcrypt

class User(BaseModel):
    """Represents a user in the system."""
    _emails = set()

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """Initializes a user with name, email validation, and password hashing."""
        super().__init__()
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        # Hash the password immediately upon creation
        self.hash_password(password)

    def validate_name(self, value, field_name):
        """Ensures the name is not empty and does not exceed 50 characters."""
        if not value or len(value) > 50:
            raise ValueError(f"{field_name} is required (max 50 characters).")
        return value
    
    def validate_email(self, email):
        """Validates the email format and ensures its uniqueness."""
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")
        if email in User._emails:
            raise ValueError("Email must be unique.")
        User._emails.add(email)
        return email

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the stored hashed password."""
        return bcrypt.check_password_hash(self.password, password)