# 📋 Testing Report - HBnB Evolution (Part 2)

## 1. Introduction
Ce rapport documente les tests effectués sur l'API HBnB pour valider la logique métier, l'intégrité des données et les codes de réponse HTTP. Les tests ont été réalisés via des scripts automatisés (**Python Unittest**) et des vérifications manuelles (**cURL**).

## 2. Environnement de Test
* **Framework de test** : Python `unittest`
* **Outils additionnels** : `cURL`, Flask-RESTx (Swagger)
* **Base de données** : In-Memory Repository (Simulation)

---

## 3. Scénarios de Test et Résultats

### A. Gestion des Utilisateurs (Users)
| Cas de test | Données d'entrée | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| Création valide | first_name, last_name, email corrects | 201 Created | ✅ Passé |
| Format Email | email: "invalid-mail" | 400 Bad Request | ✅ Passé |
| Champs obligatoires | first_name: "" | 400 Bad Request | ✅ Passé |

### B. Gestion des Lieux (Places)
| Cas de test | Données d'entrée | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| Prix positif | price: -10 | 400 Bad Request | ✅ Passé |
| Type de prix | price: "cent" (string) | 400 Bad Request | ✅ Passé |
| Latitude bornée | latitude: 120 | 400 Bad Request | ✅ Passé |
| Coordonnées (type) | latitude: "nord" | 400 Bad Request | ✅ Passé |

### C. Gestion des Avis (Reviews)
| Cas de test | Données d'entrée | Résultat attendu | État |
| :--- | :--- | :--- | :--- |
| Note valide | rating: 5 | 201 Created | ✅ Passé |
| Note hors bornes | rating: 6 | 400 Bad Request | ✅ Passé |
| Note (type) | rating: 4.5 (float) | 400 Bad Request | ✅ Passé |

---

## 4. Preuve d'exécution (Console Output)

```bash
root@hbnb:~/holbertonschool-hbnb/part2/hbnb# export PYTHONPATH=$(pwd)
root@hbnb:~/holbertonschool-hbnb/part2/hbnb# python3 tests/test_api.py
......
----------------------------------------------------------------------
Ran 6 tests in 0.206s

OK
```

## 5. Conclusion
Tous les points de contrôle de la **Task 6** ont été validés. L'API rejette systématiquement les données mal formées ou de type incorrect (grâce aux vérifications `isinstance` et aux bornes numériques dans la Façade) et renvoie les codes HTTP appropriés.
