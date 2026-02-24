import re
from app.models.base_model import BaseModel

class User(BaseModel):
    _emails = set()

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.is_admin = is_admin

    def validate_name(self, value, field_name):
        if not value or len(value) > 50:
            raise ValueError(f"{field_name} is required and must be <= 50 characterss.")
        return value
    
    def validate_email(self, email):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")
        
        if email in User._emails:
            raise ValueError("Email must be unique.")
        
        User._emails.add(email)
        return email
