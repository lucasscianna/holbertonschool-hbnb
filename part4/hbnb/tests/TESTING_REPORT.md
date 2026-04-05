# 📋 Testing Report - HBnB Evolution (Part 3)

## 1. Introduction

Ce rapport documente les tests effectués sur l'API HBnB pour valider la logique métier, l'intégrité des données et les codes de réponse HTTP. Les tests couvrent la migration vers SQLAlchemy (T6 à T10), les tests unitaires par couche, et les tests end-to-end de l'API. Les tests ont été réalisés via des scripts automatisés (**Python Unittest / Pytest**) et des vérifications manuelles (**cURL**).

---

## 2. Environnement de Test

- **Framework de test** : Python `unittest` + `pytest`
- **Outils additionnels** : `cURL`, Flask-RESTx (Swagger)
- **Base de données (production)** : SQLite via SQLAlchemy ORM
- **Base de données (tests)** : SQLite en mémoire (`sqlite:///:memory:`) avec `StaticPool`
- **Authentification** : Flask-JWT-Extended
- **Hashage** : Flask-Bcrypt

---

## 3. Architecture des Tests

```
tests/
├── test_api.py           # Tests end-to-end (14 tests)
├── test_models.py        # Tests unitaires — validations des modèles (18 tests)
├── test_repositories.py  # Tests unitaires — CRUD base de données (8 tests)
├── test_facade.py        # Tests unitaires — logique métier (16 tests)
└── test_endpoints.py     # Tests unitaires — routes API (18 tests)
```

**Total : 74 tests**

---

## 4. Scénarios de Test et Résultats

### A. Tests des Modèles (`test_models.py`) — 18/18 ✅

#### User

| Cas de test | Données d'entrée | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| Création valide | first_name, last_name, email corrects | Instance créée | ✅ Passé |
| first_name vide | first_name: "" | ValueError | ✅ Passé |
| first_name trop long | first_name: 51 caractères | ValueError | ✅ Passé |
| Email invalide | email: "not-an-email" | ValueError | ✅ Passé |
| Password hashé | password: "password123" | Hash bcrypt ($2b$) | ✅ Passé |
| Vérification password correct | verify_password("password123") | True | ✅ Passé |
| Vérification password incorrect | verify_password("wrong") | False | ✅ Passé |

#### Place

| Cas de test | Données d'entrée | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| Création valide | Tous les champs corrects | Instance créée | ✅ Passé |
| Titre vide | title: "" | ValueError | ✅ Passé |
| Prix négatif | price: -5.0 | ValueError | ✅ Passé |
| Latitude invalide | latitude: 200.0 | ValueError | ✅ Passé |
| Longitude invalide | longitude: 500.0 | ValueError | ✅ Passé |

#### Review

| Cas de test | Données d'entrée | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| Rating trop élevé | rating: 6 | ValueError | ✅ Passé |
| Rating trop bas | rating: 0 | ValueError | ✅ Passé |
| Texte vide | text: "" | ValueError | ✅ Passé |

#### Amenity

| Cas de test | Données d'entrée | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| Création valide | name: "WiFi" | Instance créée | ✅ Passé |
| Nom vide | name: "" | ValueError | ✅ Passé |
| Nom trop long | name: 51 caractères | ValueError | ✅ Passé |

---

### B. Tests des Repositories (`test_repositories.py`) — 8/8 ✅

| Cas de test | Description | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| add() + get() | Ajout puis récupération par ID | Objet retourné | ✅ Passé |
| get() inexistant | ID inconnu | None | ✅ Passé |
| get_all() | 2 users ajoutés | Liste de 2 | ✅ Passé |
| update() | Modification d'un attribut | Attribut mis à jour | ✅ Passé |
| delete() | Suppression d'un objet | None après delete | ✅ Passé |
| get_by_attribute() | Recherche par email | Objet retourné | ✅ Passé |
| get_user_by_email() found | Email existant | User retourné | ✅ Passé |
| get_user_by_email() not found | Email inconnu | None | ✅ Passé |

---

### C. Tests de la Facade (`test_facade.py`) — 16/16 ✅

#### Users

| Cas de test | Description | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| create_user() valide | Données correctes | User avec ID | ✅ Passé |
| Premier user = admin | 1er user créé | is_admin: True | ✅ Passé |
| Deuxième user non admin | 2ème user créé | is_admin: False | ✅ Passé |
| Email dupliqué | Même email 2x | ValueError | ✅ Passé |
| Email invalide | email: "not-an-email" | ValueError | ✅ Passé |
| get_user() | ID existant | User retourné | ✅ Passé |
| get_user_by_email() | Email existant | User retourné | ✅ Passé |
| get_all_users() | 2 users créés | Liste de 2 | ✅ Passé |
| update_user() | Modification first_name | Attribut mis à jour | ✅ Passé |
| update_user() inexistant | ID inconnu | None | ✅ Passé |

#### Places

| Cas de test | Description | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| create_place() valide | Données correctes | Place créée | ✅ Passé |
| Prix négatif | price: -10.0 | ValueError | ✅ Passé |
| Owner inexistant | owner_id inconnu | ValueError | ✅ Passé |
| get_place() | ID existant | Place retournée | ✅ Passé |

#### Amenities

| Cas de test | Description | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| create_amenity() valide | name: "WiFi" | Amenity créée | ✅ Passé |
| Nom vide | name: "" | ValueError | ✅ Passé |
| get_all_amenities() | 2 amenities créées | Liste retournée | ✅ Passé |

---

### D. Tests des Endpoints (`test_endpoints.py`) — 18/18 ✅

#### Users

| Cas de test | Méthode + Route | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| Création valide | POST /api/v1/users/ | 201 + id sans password | ✅ Passé |
| Champ manquant | POST /api/v1/users/ | 400 | ✅ Passé |
| Email invalide | POST /api/v1/users/ | 400 | ✅ Passé |
| Email dupliqué | POST /api/v1/users/ | 400 | ✅ Passé |
| Récupération par ID | GET /api/v1/users/\<id\> | 200 | ✅ Passé |
| ID inexistant | GET /api/v1/users/fake | 404 | ✅ Passé |
| Liste tous les users | GET /api/v1/users/ | 200 + liste | ✅ Passé |
| Mise à jour (propriétaire) | PUT /api/v1/users/\<id\> | 200 + données màj | ✅ Passé |
| Mise à jour (autre user) | PUT /api/v1/users/\<id\> | 403 | ✅ Passé |

#### Places

| Cas de test | Méthode + Route | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| Création valide | POST /api/v1/places/ | 201 | ✅ Passé |
| Prix négatif | POST /api/v1/places/ | 400 | ✅ Passé |
| Sans token JWT | POST /api/v1/places/ | 401 | ✅ Passé |
| Liste toutes les places | GET /api/v1/places/ | 200 | ✅ Passé |
| ID inexistant | GET /api/v1/places/fake | 404 | ✅ Passé |

#### Amenities

| Cas de test | Méthode + Route | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| Création (admin) | POST /api/v1/amenities/ | 201 | ✅ Passé |
| Création (non admin) | POST /api/v1/amenities/ | 403 | ✅ Passé |
| Liste toutes | GET /api/v1/amenities/ | 200 | ✅ Passé |

---

### E. Tests End-to-End (`test_api.py`) — 14/14 ✅

| Cas de test | Description | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| Création user valide | 1er user = admin auto | 201 | ✅ Passé |
| Email invalide | Format incorrect | 400 | ✅ Passé |
| User inexistant | GET id inconnu | 404 | ✅ Passé |
| Prix négatif (place) | price: -5.0 | 400 | ✅ Passé |
| Rating invalide (review) | rating: 7 | 400 | ✅ Passé |
| Autorisation (place) | Jane modifie place de John | 403 | ✅ Passé |
| Privilèges admin | Non-admin crée amenity | 403 | ✅ Passé |
| T6 — User persisté en DB | User sauvegardé SQLAlchemy | 201 + id | ✅ Passé |
| T6 — Password non retourné | Réponse sans password | Pas de champ password | ✅ Passé |
| T6 — Email dupliqué | Même email 2x | 400 | ✅ Passé |
| T6 — Get user par ID | Depuis la DB | 200 | ✅ Passé |
| T6 — Get all users | Liste depuis DB | 200 + liste | ✅ Passé |
| T6 — Update user | Persisté en base | 200 + données | ✅ Passé |
| T6 — Premier user admin | is_admin=True | 201 | ✅ Passé |

---

## 5. Preuve d'exécution (Console Output)

### Tests unitaires + end-to-end (74 tests)

```bash
root@hbnb:~/holbertonschool-hbnb/part3/hbnb# python3 -m pytest tests/test_models.py tests/test_repositories.py tests/test_facade.py tests/test_endpoints.py -v

============================================================= test session starts ==============================================================
platform linux -- Python 3.10.12, pytest-9.0.2, pluggy-1.6.0
collected 60 items

tests/test_models.py::TestUserModel::test_invalid_email_format PASSED
tests/test_models.py::TestUserModel::test_invalid_first_name_empty PASSED
tests/test_models.py::TestUserModel::test_invalid_first_name_too_long PASSED
tests/test_models.py::TestUserModel::test_password_hashed PASSED
tests/test_models.py::TestUserModel::test_valid_user PASSED
tests/test_models.py::TestUserModel::test_verify_password_correct PASSED
tests/test_models.py::TestUserModel::test_verify_password_wrong PASSED
tests/test_models.py::TestPlaceModel::test_invalid_latitude PASSED
tests/test_models.py::TestPlaceModel::test_invalid_longitude PASSED
tests/test_models.py::TestPlaceModel::test_invalid_price_negative PASSED
tests/test_models.py::TestPlaceModel::test_invalid_title_empty PASSED
tests/test_models.py::TestPlaceModel::test_valid_place PASSED
tests/test_models.py::TestReviewModel::test_invalid_rating_too_high PASSED
tests/test_models.py::TestReviewModel::test_invalid_rating_too_low PASSED
tests/test_models.py::TestReviewModel::test_invalid_text_empty PASSED
tests/test_models.py::TestAmenityModel::test_invalid_name_empty PASSED
tests/test_models.py::TestAmenityModel::test_invalid_name_too_long PASSED
tests/test_models.py::TestAmenityModel::test_valid_amenity PASSED
tests/test_repositories.py::TestSQLAlchemyRepository::test_add_and_get PASSED
tests/test_repositories.py::TestSQLAlchemyRepository::test_delete PASSED
tests/test_repositories.py::TestSQLAlchemyRepository::test_get_all PASSED
tests/test_repositories.py::TestSQLAlchemyRepository::test_get_by_attribute PASSED
tests/test_repositories.py::TestSQLAlchemyRepository::test_get_nonexistent PASSED
tests/test_repositories.py::TestSQLAlchemyRepository::test_update PASSED
tests/test_repositories.py::TestUserRepository::test_get_user_by_email_found PASSED
tests/test_repositories.py::TestUserRepository::test_get_user_by_email_not_found PASSED
tests/test_facade.py::TestUserFacade::test_create_user_duplicate_email PASSED
tests/test_facade.py::TestUserFacade::test_create_user_first_is_admin PASSED
tests/test_facade.py::TestUserFacade::test_create_user_invalid_email PASSED
tests/test_facade.py::TestUserFacade::test_create_user_second_not_admin PASSED
tests/test_facade.py::TestUserFacade::test_create_user_valid PASSED
tests/test_facade.py::TestUserFacade::test_get_all_users PASSED
tests/test_facade.py::TestUserFacade::test_get_user PASSED
tests/test_facade.py::TestUserFacade::test_get_user_by_email PASSED
tests/test_facade.py::TestUserFacade::test_update_user PASSED
tests/test_facade.py::TestUserFacade::test_update_user_not_found PASSED
tests/test_facade.py::TestPlaceFacade::test_create_place_invalid_price PASSED
tests/test_facade.py::TestPlaceFacade::test_create_place_owner_not_found PASSED
tests/test_facade.py::TestPlaceFacade::test_create_place_valid PASSED
tests/test_facade.py::TestPlaceFacade::test_get_place PASSED
tests/test_facade.py::TestAmenityFacade::test_create_amenity_empty_name PASSED
tests/test_facade.py::TestAmenityFacade::test_create_amenity_valid PASSED
tests/test_facade.py::TestAmenityFacade::test_get_all_amenities PASSED
tests/test_endpoints.py::TestUserEndpoints::test_get_all_users_200 PASSED
tests/test_endpoints.py::TestUserEndpoints::test_get_user_200 PASSED
tests/test_endpoints.py::TestUserEndpoints::test_get_user_404 PASSED
tests/test_endpoints.py::TestUserEndpoints::test_post_user_201 PASSED
tests/test_endpoints.py::TestUserEndpoints::test_post_user_400_duplicate_email PASSED
tests/test_endpoints.py::TestUserEndpoints::test_post_user_400_invalid_email PASSED
tests/test_endpoints.py::TestUserEndpoints::test_post_user_400_missing_field PASSED
tests/test_endpoints.py::TestUserEndpoints::test_put_user_200 PASSED
tests/test_endpoints.py::TestUserEndpoints::test_put_user_403_wrong_user PASSED
tests/test_endpoints.py::TestPlaceEndpoints::test_get_all_places_200 PASSED
tests/test_endpoints.py::TestPlaceEndpoints::test_get_place_404 PASSED
tests/test_endpoints.py::TestPlaceEndpoints::test_post_place_201 PASSED
tests/test_endpoints.py::TestPlaceEndpoints::test_post_place_400_negative_price PASSED
tests/test_endpoints.py::TestPlaceEndpoints::test_post_place_401_no_token PASSED
tests/test_endpoints.py::TestAmenityEndpoints::test_get_all_amenities_200 PASSED
tests/test_endpoints.py::TestAmenityEndpoints::test_post_amenity_201_as_admin PASSED
tests/test_endpoints.py::TestAmenityEndpoints::test_post_amenity_403_not_admin PASSED

================================================== 60 passed, 20 warnings in 63.41s ==================================================
```

### Test end-to-end (14 tests)

```bash
root@hbnb:~/holbertonschool-hbnb/part3/hbnb# python3 -m pytest tests/test_api.py -v

============================================================= test session starts ==============================================================
collected 14 items

tests/test_api.py::TestHBnBAPI::test_admin_privileges PASSED
tests/test_api.py::TestHBnBAPI::test_authorization_logic PASSED
tests/test_api.py::TestHBnBAPI::test_duplicate_email_rejected PASSED
tests/test_api.py::TestHBnBAPI::test_first_user_is_admin PASSED
tests/test_api.py::TestHBnBAPI::test_get_all_users PASSED
tests/test_api.py::TestHBnBAPI::test_get_non_existent_user PASSED
tests/test_api.py::TestHBnBAPI::test_get_user_by_id PASSED
tests/test_api.py::TestHBnBAPI::test_password_not_returned PASSED
tests/test_api.py::TestHBnBAPI::test_place_invalid_price PASSED
tests/test_api.py::TestHBnBAPI::test_review_invalid_rating PASSED
tests/test_api.py::TestHBnBAPI::test_update_user PASSED
tests/test_api.py::TestHBnBAPI::test_user_creation_invalid_email PASSED
tests/test_api.py::TestHBnBAPI::test_user_creation_valid PASSED
tests/test_api.py::TestHBnBAPI::test_user_persisted_in_db PASSED

================================================== 14 passed, 7 warnings in 32.67s ==================================================
```

---

## 6. Récapitulatif Global

| Fichier de test | Couche testée | Tests | Résultat |
| :--- | :--- | :--- | :--- |
| `test_models.py` | Modèles / Validations | 18 | ✅ 18/18 |
| `test_repositories.py` | Repositories / CRUD DB | 8 | ✅ 8/8 |
| `test_facade.py` | Facade / Logique métier | 16 | ✅ 16/16 |
| `test_endpoints.py` | API Endpoints / Routes | 18 | ✅ 18/18 |
| `test_api.py` | End-to-End / Intégration | 14 | ✅ 14/14 |
| **Total** | **Toutes couches** | **74** | **✅ 74/74** |

---

## 7. Conclusion

Tous les tests de la **Part 3** ont été validés avec succès. La migration vers SQLAlchemy (T6 à T8) a été réalisée sans régression. Les entités `User`, `Place`, `Review` et `Amenity` sont correctement mappées en base de données avec leurs relations (one-to-many et many-to-many). La couverture des tests couvre les 4 couches de l'application :

- **Modèles** : toutes les validations métier sont correctement appliquées via `@validates`
- **Repositories** : les opérations CRUD SQLAlchemy fonctionnent correctement
- **Facade** : la logique métier (admin auto, email unique, ownership) est validée
- **API** : les codes HTTP (200, 201, 400, 401, 403, 404) sont correctement retournés

> ⚠️ Note : `Place` et `Amenity` utilisent encore `InMemoryRepository` mais ce sera migré dans la partie 4 probablement