import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        def save(self):
            """Update the updated_at timestamp"""
            self.updated_at = datetime.now()
        
        def update(self, data):
            """Update attributes using a dictionary"""
            self.updated_at = datetime.now()
        
        def update(self, data):
            """Update attributes using a dictionnary"""
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            self.save()
