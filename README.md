# 🏨 HBnB Evolution : Full-Stack Service Clone

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-RESTx-lightgrey?style=for-the-badge&logo=flask)
![SQLAlchemy](https://img.shields.io/badge/Database-SQLAlchemy-red?style=for-the-badge)
![Docker](https://img.shields.io/badge/Deployment-Docker-blue?style=for-the-badge&logo=docker)

> **Un clone complet de la plateforme AirBnB, conçu avec une architecture modulaire et évolutive au cours du cursus Holberton School.**

## 📌 Vue d'ensemble du Projet
HBnB Evolution est un projet fil rouge divisé en quatre phases majeures. L'objectif est de construire une application web robuste en partant du diagramme de classes jusqu'au déploiement final.

---

## 🗺️ Phase 1 : Conception & UML
- **Objectif :** Définir l'architecture technique et les relations entre les entités (User, Place, Review, Amenity).
- **Livrables :** Diagrammes de classes UML et conception de l'architecture en couches (Buisness Logic, Persistence, API).

## ⚙️ Phase 2 : Business Logic & API RESTful
- **Objectif :** Implémentation du cœur de l'application.
- **Points clés :**
  - Utilisation du **Facade Pattern** pour séparer la logique métier de l'API.
  - Création d'une API REST avec **Flask-RESTx**.
  - Validation stricte des données (types, formats, contraintes métier).
  - Tests unitaires complets (`unittest`).

## 🗄️ Phase 3 : Authentification & Base de Données (En cours)
- **Objectif :** Passer d'un stockage en mémoire à une persistance réelle.
- **Points clés :**
  - Intégration de **SQLAlchemy** et MySQL.
  - Sécurisation des accès via **JWT (JSON Web Tokens)**.
  - Gestion des mots de passe hachés.

## 🚀 Phase 4 : Déploiement & Client Web
- **Objectif :** Rendre l'application accessible et créer l'interface utilisateur.
- **Points clés :**
  - Conteneurisation avec **Docker** et orchestration avec **Docker Compose**.
  - Configuration d'un serveur proxy inverse (**Nginx**).
  - Développement du front-end dynamique (HTML/CSS/JS).

---

## 🧪 Installation et Tests (Phase 2)
1. **Installation :** `pip install -r requirements.txt`
2. **Lancer l'API :** `python3 run.py`
3. **Tests :** `export PYTHONPATH=$(pwd) && python3 tests/test_api.py`

## 🧠 Compétences acquises
- Architecture logicielle (Clean Architecture).
- Développement d'API REST sécurisées.
- Gestion de bases de données relationnelles.
- DevOps (Docker, Nginx).

---
*Projet réalisé par **Lucas Scianna** et **Ilan Cornibe**- Étudiants en développement logiciel à Holberton School.*
