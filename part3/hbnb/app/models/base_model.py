from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    """Classe de base pour tous les modèles HBNB."""

    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        """Initialise une nouvelle instance avec un ID unique et des horodatages."""
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

    def update(self, data):
        """Met à jour les attributs de l'instance à partir d'un dictionnaire."""
        protected_fields = ['id', 'created_at', 'updated_at']
        
        for key, value in data.items():
            if hasattr(self, key) and key not in protected_fields:
                setattr(self, key, value)