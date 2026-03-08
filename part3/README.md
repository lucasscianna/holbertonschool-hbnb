HBnB Evolution: Part 3 - Enhanced Backend & Database Integration
📌 Présentation du Projet
Bienvenue dans la troisième phase du projet HBnB. Après avoir prototypé l'application avec un stockage en mémoire, cette étape marque la transition vers un système de grade industriel. L'objectif est de sécuriser l'application via une authentification robuste et d'assurer la persistance des données grâce à une intégration SQL complète.

Cette partie transforme le projet d'un simple script en une API REST sécurisée et scalable, prête pour un déploiement en production.

🚀 Objectifs Principaux
1. Authentification & Autorisation (Sécurité)
JWT (JSON Web Tokens) : Mise en œuvre de Flask-JWT-Extended pour gérer les sessions utilisateurs de manière stateless.

Sécurité des Mots de Passe : Utilisation de bcrypt pour le hachage des mots de passe. Aucun mot de passe n'est stocké en clair.

Contrôle d'Accès (RBAC) : Distinction entre les utilisateurs standards et les administrateurs via l'attribut is_admin.

2. Persistance des Données (Base de données)
SQLAlchemy ORM : Transition complète des listes Python vers une abstraction de base de données relationnelle.

Stratégie Multi-Environnement :

Développement : Utilisation de SQLite (léger, fichier local).

Production : Configuration prête pour MySQL.

Gestion des Relations : Mapping complexe des relations (User -> Places, Place -> Reviews, Place <-> Amenities).

🏗️ Architecture du Système
Schéma de la Base de Données (ER Diagram)
Le schéma a été conçu pour garantir l'intégrité référentielle. Voici la visualisation des entités :

Users : Gèrent les informations de profil et l'authentification.

Places : Liés à un propriétaire (User) et contiennent des avis et des commodités.

Reviews : Relient un utilisateur à un lieu spécifique.

Amenities : Relation "Many-to-Many" avec les lieux.

📂 Structure du Répertoire
🛡️ Endpoints & Sécurité
Authentification
Opérations Protégées (Exemples)
🛠️ Installation et Configuration
Clonage et Environnement :

Dépendances :

Variables d'Environnement :
Configure ton environnement pour choisir la base de données :

Lancement :

🧪 Tests
Les tests couvrent désormais la couche de persistance :

Vérification que les mots de passe sont bien hachés en base.

Test de l'expiration des tokens JWT.

Validation des contraintes FOREIGN KEY (ex: impossible de supprimer un utilisateur s'il possède des lieux actifs sans gestion de cascade).