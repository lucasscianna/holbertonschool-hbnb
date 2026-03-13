from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Interface abstraite définissant le contrat d'un dépôt de données.

    Cette classe suit le Repository Pattern pour isoler la couche de persistance
    de la logique métier.
    """

    @abstractmethod
    def add(self, obj):
        """
        Ajoute un nouvel objet au dépôt.

        :param obj: L'objet à stocker (doit posséder un attribut 'id').
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Récupère un objet par son identifiant unique.

        :param obj_id: L'identifiant de l'objet.
        :return: L'objet correspondant ou None s'il n'existe pas.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Récupère tous les objets présents dans le dépôt.

        :return: Une liste contenant tous les objets.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Met à jour un objet existant avec de nouvelles données.

        :param obj_id: L'identifiant de l'objet à modifier.
        :param data: Un dictionnaire contenant les attributs à mettre à jour.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Supprime un objet du dépôt.

        :param obj_id: L'identifiant de l'objet à supprimer.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Recherche un objet selon la valeur d'un attribut spécifique.

        :param attr_name: Nom de l'attribut à vérifier.
        :param attr_value: Valeur recherchée pour cet attribut.
        :return: Le premier objet correspondant ou None.
        """
        pass


class InMemoryRepository(Repository):
    """
    Implémentation concrète du Repository utilisant un dictionnaire en mémoire.
    """

    def __init__(self):
        """Initialise le stockage interne sous forme de dictionnaire."""
        super().__init__(Amenity)

    def add(self, obj):
        """Ajoute un objet au dictionnaire interne en utilisant son ID."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Récupère l'objet via sa clé dans le dictionnaire."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Retourne la liste des valeurs du dictionnaire."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Met à jour l'objet récupéré.
        
        Note : L'objet doit implémenter une méthode update(data).
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Supprime l'entrée correspondante si l'ID existe."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Parcourt les objets pour trouver une correspondance d'attribut."""
        return next(
            (obj for obj in self._storage.values() 
             if getattr(obj, attr_name) == attr_value), 
            None
        )
