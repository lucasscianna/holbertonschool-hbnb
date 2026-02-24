"""
Module Facade qui centralise la logique métier et la communication
entre la couche de présentation et la persistance.
"""

from app.persistence.repository import InMemoryRepository
from app.models.user import User


class HBnBFacade:
    """Façade pour gérer les interactions avec les modèles HBnB."""

    def __init__(self):
        """Initialisation des dépôts pour chaque entité."""
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Crée et enregistre un nouvel utilisateur."""
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email')
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Récupère un utilisateur par son identifiant unique."""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Récupère la liste complète des utilisateurs."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Met à jour les informations d'un utilisateur existant."""
        return self.user_repo.update(user_id, user_data)
