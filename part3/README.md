# HBnB Evolution: Part 3 - Enhanced Backend & Database Integration

## 📌 Présentation du Projet
Bienvenue dans la troisième phase du projet **HBnB**. Après avoir prototypé l'application avec un stockage en mémoire, cette étape marque la transition vers un système de grade industriel. L'objectif est de sécuriser l'application via une authentification robuste et d'assurer la persistance des données grâce à une intégration SQL complète via **SQLAlchemy**.

---

## 🚀 Objectifs Principaux

### 🛡️ Authentification & Autorisation (Sécurité)
* **JWT (JSON Web Tokens) :** Mise en œuvre de `Flask-JWT-Extended` pour la gestion des sessions.
* **Sécurité des Mots de Passe :** Hachage systématique avec `bcrypt`.
* **Contrôle d'Accès (RBAC) :** Gestion des privilèges via l'attribut `is_admin`.

### 💾 Persistance des Données (Base de données)
* **SQLAlchemy ORM :** Mapping objet-relationnel pour toutes les entités.
* **Stratégie Multi-Environnement :** Utilisation de **SQLite** pour le développement et configuration de **MySQL** pour la production.
* **Validation & Intégrité :** Mise en place de contraintes de clé étrangère (FOREIGN KEY) et de règles d'unicité.

---

## 🏗️ Architecture & Arborescence du Projet

Le projet suit une structure modulaire pour séparer la logique métier, la persistance et l'API.



```text
hbnb/
├── api/
│   ├── v1/
│   │   ├── auth/           # Gestion de la connexion et des tokens
│   │   ├── users/          # Endpoints utilisateurs (Inscription/Profil)
│   │   ├── places/         # Endpoints lieux (Protégés par JWT)
│   │   └── ...
├── models/
│   ├── base_model.py       # Classe mère avec SQLAlchemy
│   ├── user.py             # Modèle User avec hachage password
│   ├── place.py            # Modèle Place avec relations
│   ├── review.py           # Modèle Review
│   └── amenity.py          # Modèle Amenity
├── persistence/
│   ├── db_repository.py    # Logique d'interaction avec la DB
│   └── repository.py       # Interface de dépôt abstraite
├── config.py               # Configuration (Dev vs Prod)
└── app.py                  # Point d'entrée de l'application
---

## 🔐 Endpoints & Sécurité

### Authentification
| Méthode | Endpoint | Description | Accès |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/v1/auth/login` | Génération du token JWT | Public |
| **POST** | `/api/v1/users/` | Inscription nouvel utilisateur | Public |

### Opérations Protégées
| Méthode | Endpoint | Description | Condition |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/v1/places/` | Créer un lieu | Token valide requis |
| **PUT** | `/api/v1/places/<id>` | Modifier un lieu | Propriétaire / Admin |
| **DELETE** | `/api/v1/amenities/<id>` | Supprimer un équipement | **Admin seul** |

---

## 🛠️ Installation et Configuration

### 1. Clonage du dépôt
```bash
git clone [https://github.com/votre-repo/holbertonschool-hbnb.git](https://github.com/votre-repo/holbertonschool-hbnb.git)
cd holbertonschool-hbnb

### 2. Configuration de l'environnement

```bash
# Création et activation de l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installation des dépendances
pip install -r requirements.txt

### 3. Variables d'environnement

Configurez le moteur de stockage pour utiliser la base de données :

```bash
export HBNB_TYPE_STORAGE=db
export JWT_SECRET_KEY=votre_cle_secrete


## 🧪 Stratégie de Tests

Pour garantir la stabilité du système, les tests se concentrent sur :

* **Sécurité** : Vérification que les mots de passe sont hachés en base (pas de texte clair).
* **Authentification** : Test de validité et d'expiration des tokens JWT.
* **Intégrité SQL** : Validation des contraintes de clés étrangères et suppression en cascade.
* **Autorisation** : Tentative d'accès à une route Admin avec un compte utilisateur standard.

### Exécution des tests

Nous utilisons **pytest** pour la suite de tests. Pour les lancer, assurez-vous d'être dans votre environnement virtuel et exécutez :

```bash
# Lancer tous les tests
pytest

# Lancer avec les détails des logs
pytest -v

# Vérifier la couverture de code (si pytest-cov est installé)
pytest --cov=app tests/


## 📚 Ressources

* [Flask-JWT-Extended Docs](https://flask-jwt-extended.readthedocs.io/)
* [SQLAlchemy ORM Docs](https://docs.sqlalchemy.org/en/20/)
* [Mermaid.js (ER Diagrams)](https://mermaid.js.org/syntax/entityRelationshipDiagram.html)