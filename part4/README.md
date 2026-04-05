# HBnB - Partie 4 : Le Client Web Simple (Frontend)

Bienvenue dans la **Partie 4** du projet HBnB ! Cette étape consiste à développer l'interface utilisateur (Frontend) complète permettant de communiquer avec notre API Backend Flask conçue dans les parties précédentes.

## 🚀 Objectifs du projet

L'objectif de ce module est de construire un "Simple Web Client" fonctionnel en `HTML`, `CSS` et `JavaScript` natif (Vanilla JS), en respectant les principes d'une application dynamique.

Les missions principales accomplies sont :
1. **Intégration HTML/CSS** : Mise en place d'un design responsive, moderne et épuré.
2. **Système de Connexion (Login)** : Formulaire fonctionnel envoyant les identifiants à l'API et stockant le **JWT_TOKEN** dans les cookies.
3. **Consommation de l'API (Fetch)** : 
    - Récupération de la liste des lieux disponibles (`index.html`).
    - Récupération des informations détaillées d'un lieu et de ses avis (`place.html`).
    - Ajout de nouveaux avis via les routes protégées nécessitant une authentification (`add_review.html`).
4. **Filtres Dynamiques** : Filtrage des logements par prix côté client sans rechargement de page.

## 📁 Architecture des Fichiers

```text
part4/
│
├── index.html          # Page d'accueil avec la liste des lieux et les filtres.
├── login.html          # Page du formulaire de connexion.
├── place.html          # Page de détails d'un lieu et de ses commentaires.
├── add_review.html     # Formulaire d'ajout de commentaires (protégé).
├── styles.css          # Feuille de style principale (Design system).
│
├── scripts.js          # Fonctions utilitaires partagées (gestion des cookies, etc).
└── scripts/
    ├── index.js        # Logique de chargement des lieux et du filtre de prix.
    ├── login.js        # Logique de soumission de l'authentification.
    ├── place.js        # Chargement détaillé d'un lieu via son ID en URL.
    └── review.js       # Logique d'envoi d'un nouveau commentaire sous JWT Token.
```

## 🛠️ Instructions pour Lancer l'Application

Le Frontend a besoin du Backend pour récupérer la donnée. Vous devez faire tourner les deux environnements en parallèle.

### 1. Démarrer l'API (Backend)
Dans un premier terminal, naviguez dans le dossier `part4/hbnb` et lancez le serveur Flask Python :
```bash
cd part4/hbnb
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run.py
```
*(L'API devrait tourner sur `http://127.0.0.1:5000`)*

### 2. Démarrer le Frontend
Ouvrez le fichier `index.html` dans Visual Studio Code et utilisez l'extension **Live Server** (bouton "Go Live" en bas à droite).
Celui-ci va ouvrir l'application dans votre navigateur (généralement sur le port `5500` ou `3000`).

### 3. Connexion de Test
Si vous avez lancé le fichier `seed_db.py` pour pré-remplir la base, vous pouvez tester la connexion avec le compte suivant :
- **Email** : `alice@hbnb.com`
- **Mot de passe** : `password123`

## 🧪 Tests

Des tests E2E (End-to-End) avec Selenium WebDriver ainsi que des tests unitaires structurels ont été conçus pour éprouver le Frontend. Ils se trouvent dans le registre `part4/hbnb/tests/`.

---
> Modélisé et conçu dans le cadre du projet HBnB d'Holberton School.
