The HBnB Evolution project is a modular application that follows a layered architecture to ensure maintainability and scalability.

The purpose of this document is to describe the core entities of the Business Logic Layer.

It contains a class diagram detailing the system’s main domain models, their attributes, inheritance relationships, and associations.

```mermaid
classDiagram
direction TB

class BaseEntity {
    +id : UUID
    +created_at : datetime
    +updated_at : datetime
}

class User {
    +first_name : string
    +last_name : string
    +email : string
    +password : string
    +is_admin : boolean
}

class Place {
    +title : string
    +description : string
    +price : float
    +latitude : float
    +longitude : float
}

class Review {
    +rating : int
    +comment : string
}

class Amenity {
    +name : string
    +description : string
}

BaseEntity <|-- User
BaseEntity <|-- Place
BaseEntity <|-- Review
BaseEntity <|-- Amenity

User --> Place : owns
Place --> Review : has
User --> Review : writes
Place --> Amenity : includes
```
Business Logic Layer – Class Diagram

This diagram describes the core entities of the HBnB Business Logic layer.

All entities inherit from BaseEntity, which provides a unique identifier and timestamps for audit purposes.

The relationships between entities reflect the business rules, including ownership of places, user reviews, and place amenities.