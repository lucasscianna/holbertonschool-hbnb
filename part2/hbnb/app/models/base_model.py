import uuid
from datetime import datetime

class BaseModel:
    """Classe de base pour tous les modèles HBNB."""

    def __init__(self):
        """Initialise une nouvelle instance avec un ID unique et des horodatages."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Met à jour l'horodatage updated_at au moment actuel."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Met à jour les attributs de l'instance à partir d'un dictionnaire."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
