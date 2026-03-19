# HBnB — Entity-Relationship Diagram
```mermaid
erDiagram
  USER {
    char id PK
    varchar first_name
    varchar last_name
    varchar email
    varchar password
    boolean is_admin
  }
  PLACE {
    char id PK
    varchar title
    text description
    decimal price
    float latitude
    float longitude
    char owner_id FK
  }
  REVIEW {
    char id PK
    text text
    int rating
    char user_id FK
    char place_id FK
  }
  AMENITY {
    char id PK
    varchar name
  }
  PLACE_AMENITY {
    char place_id FK
    char amenity_id FK
  }
  USER ||--o{ PLACE : "owns"
  USER ||--o{ REVIEW : "writes"
  PLACE ||--o{ REVIEW : "has"
  PLACE ||--o{ PLACE_AMENITY : "contains"
  AMENITY ||--o{ PLACE_AMENITY : "linked to"
```
# HBnB — Entity-Relationship Diagram
```mermaid
erDiagram
  USER {
    char id PK
    varchar first_name
    varchar last_name
    varchar email
    varchar password
    boolean is_admin
  }
  PLACE {
    char id PK
    varchar title
    text description
    decimal price
    float latitude
    float longitude
    char owner_id FK
  }
  REVIEW {
    char id PK
    text text
    int rating
    char user_id FK
    char place_id FK
  }
  AMENITY {
    char id PK
    varchar name
  }
  PLACE_AMENITY {
    char place_id FK
    char amenity_id FK
  }
  USER ||--o{ PLACE : "owns"
  USER ||--o{ REVIEW : "writes"
  PLACE ||--o{ REVIEW : "has"
  PLACE ||--o{ PLACE_AMENITY : "contains"
  AMENITY ||--o{ PLACE_AMENITY : "linked to"
```

## Légende

### Symboles de relation
| Notation | Signification |
|---|---|
| `\|\|` | Exactement **un** (obligatoire) |
| `o{` | **Zéro ou plusieurs** (optionnel) |
| `\|\|--o{` | Un à plusieurs |

### Clés
| Badge | Signification |
|---|---|
| `PK` | Clé primaire — identifiant unique de la table |
| `FK` | Clé étrangère — référence une autre table |

### Relations du schéma
| Relation | Type | Description |
|---|---|---|
| USER → PLACE | 1 à plusieurs | Un user peut posséder plusieurs places |
| USER → REVIEW | 1 à plusieurs | Un user peut écrire plusieurs avis |
| PLACE → REVIEW | 1 à plusieurs | Une place peut avoir plusieurs avis |
| PLACE ↔ AMENITY | Plusieurs à plusieurs | Via la table de liaison PLACE_AMENITY |

> Un user ne peut laisser qu'**un seul avis par place** (contrainte `UNIQUE` sur `user_id + place_id`).