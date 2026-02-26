import re
from app.models.base_model import BaseModel

class User(BaseModel):
    """Représente un utilisateur du système."""
    _emails = set()

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialise un utilisateur avec validation du nom et de l'email."""
        super().__init__()
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.is_admin = is_admin

    def validate_name(self, value, field_name):
        """Vérifie que le nom n'est pas vide et ne dépasse pas 50 caractères."""
        if not value or len(value) > 50:
            raise ValueError(f"{field_name} est requis (max 50 caractères).")
        return value
    
    def validate_email(self, email):
        """Valide le format de l'email et son unicité."""
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("Format d'email invalide.")
        if email in User._emails:
            raise ValueError("L'email doit être unique.")
        User._emails.add(email)
        return email
