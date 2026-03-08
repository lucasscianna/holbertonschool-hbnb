[DIÈSE] HBnB Evolution: Part 3 - Enhanced Backend & Database Integration

[DIÈSE][DIÈSE] 📌 Présentation du Projet
Bienvenue dans la troisième phase du projet HBnB. Après avoir prototypé l'application avec un stockage en mémoire, cette étape marque la transition vers un système de grade industriel. L'objectif est de sécuriser l'application via une authentification robuste et d'assurer la persistance des données grâce à une intégration SQL complète.

[DIÈSE][DIÈSE] 🚀 Objectifs Principaux

Authentification & Autorisation (Sécurité)
[ÉTOILE] JWT (JSON Web Tokens) : Mise en œuvre de Flask-JWT-Extended.
[ÉTOILE] Sécurité des Mots de Passe : Utilisation de bcrypt.
[ÉTOILE] Contrôle d'Accès (RBAC) : Attribut is_admin.

Persistance des Données (Base de données)
[ÉTOILE] SQLAlchemy ORM : Mapping des entités.
[ÉTOILE] Stratégie Multi-Environnement : SQLite (Dev) et MySQL (Prod).

[DIÈSE][DIÈSE] 🏗️ Architecture du Système

[DIÈSE][DIÈSE] 🛡️ Endpoints & Sécurité

[DIÈSE][DIÈSE][DIÈSE] Authentification
[BARRE] Méthode [BARRE] Endpoint [BARRE] Description [BARRE] Accès [BARRE]
[BARRE] :--- [BARRE] :--- [BARRE] :--- [BARRE] :--- [BARRE]
[BARRE] POST [BARRE] /api/v1/auth/login [BARRE] Connexion JWT [BARRE] Public [BARRE]
[BARRE] POST [BARRE] /api/v1/users/ [BARRE] Inscription [BARRE] Public [BARRE]

[DIÈSE][DIÈSE][DIÈSE] Opérations Protégées
[BARRE] Méthode [BARRE] Endpoint [BARRE] Description [BARRE] Condition [BARRE]
[BARRE] :--- [BARRE] :--- [BARRE] :--- [BARRE] :--- [BARRE]
[BARRE] POST [BARRE] /api/v1/places/ [BARRE] Créer un lieu [BARRE] Token requis [BARRE]
[BARRE] DELETE [BARRE] /api/v1/amenities/id [BARRE] Supprimer [BARRE] Admin seul [BARRE]

[DIÈSE][DIÈSE] 🛠️ Installation et Configuration

Clonage : git clone [URL]

Environnement : python3 -m venv venv

Dépendances : pip install -r requirements.txt

Variables : export HBNB_TYPE_STORAGE=db

[DIÈSE][DIÈSE] 🧪 Tests
[ÉTOILE] Vérification du hachage des mots de passe.
[ÉTOILE] Test de validité des tokens JWT.
[ÉTOILE] Validation des contraintes FOREIGN KEY.