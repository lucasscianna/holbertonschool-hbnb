🏡 HBnB Project – Part 2
Implementation of Business Logic and API Endpoints

📌 Description
This project is Part 2 of the HBnB application.
The goal of this phase is to implement the Presentation Layer and Business Logic Layer of the application using Python, Flask, and flask-restx.
This implementation follows a modular architecture and introduces the Facade Pattern to separate concerns between the API layer and business logic.

⚠️ Authentication (JWT) and role-based access control will be implemented in Part 3.

🏗 Architecture Overview
The application follows a layered architecture:

Client (Postman / cURL)
        ↓
API Layer (Flask + flask-restx)
        ↓
HBnBFacade (Business Logic)
        ↓
Repositories (InMemoryRepository)
        ↓
Models (User, Place, Review, Amenity)

```
hbnb/
├── app/
│   ├── __init__.py              # Initialize Flask application
│   │
│   ├── api/                     # Presentation Layer (API endpoints)
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py         # User endpoints
│   │       ├── places.py        # Place endpoints
│   │       ├── reviews.py       # Review endpoints
│   │       ├── amenities.py     # Amenity endpoints
│   │
│   ├── models/                  # Business Entities
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   ├── place.py             # Place model
│   │   ├── review.py            # Review model
│   │   ├── amenity.py           # Amenity model
│   │
│   ├── services/                # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── facade.py            # HBnBFacade (Facade Pattern)
│   │
│   ├── persistence/             # Data access layer
│       ├── __init__.py
│       ├── repository.py        # InMemoryRepository
│
├── run.py                       # Application entry point
├── config.py                    # Configuration file
├── requirements.txt             # Project dependencies
├── README.md                    # Project documentation
hbnb/
├── app/
│   ├── __init__.py              # Initialize Flask application
│   │
│   ├── api/                     # Presentation Layer (API endpoints)
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py         # User endpoints
│   │       ├── places.py        # Place endpoints
│   │       ├── reviews.py       # Review endpoints
│   │       ├── amenities.py     # Amenity endpoints
│   │
│   ├── models/                  # Business Entities
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   ├── place.py             # Place model
│   │   ├── review.py            # Review model
│   │   ├── amenity.py           # Amenity model
│   │
│   ├── services/                # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── facade.py            # HBnBFacade (Facade Pattern)
│   │
│   ├── persistence/             # Data access layer
│       ├── __init__.py
│       ├── repository.py        # InMemoryRepository
│
├── run.py                       # Application entry point
├── config.py                    # Configuration file
├── requirements.txt             # Project dependencies
├── README.md                    # Project documentation
```

🧠 Design Principles
✔ Separation of Concerns
API layer handles HTTP requests and responses.
Facade layer centralizes business logic.
Repository layer manages data persistence.
Models define the core entities.

✔ Facade Pattern
The HBnBFacade acts as an intermediary between the API and the data repositories.
It centralizes:
Data validation
Entity relationships
CRUD operations
Business rules
This ensures clean, maintainable, and scalable code.

🚀 Installation & Setup

1️⃣ Clone the repository
git clone <your-repo-url>
cd hbnb

2️⃣ Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the application
python run.py
The API will run locally (default Flask port: http://127.0.0.1:5000).

🌐 API Endpoints
All endpoints are available under:
/api/v1/

👤 Users
Method	Endpoint	Description
POST	/users	Create a new user
GET	/users	Retrieve all users
GET	/users/<id>	Retrieve a specific user

🏠 Places
Method	Endpoint	Description
POST	/places	Create a new place
GET	/places	Retrieve all places
GET	/places/<id>	Retrieve a specific place

⭐ Reviews
Method	Endpoint	Description
POST	/reviews	Create a review
GET	/reviews	Retrieve all reviews
GET	/reviews/<id>	Retrieve a specific review
DELETE	/reviews/<id>	Delete a review

🛠 Amenities
Method	Endpoint	Description
POST	/amenities	Create an amenity
GET	/amenities	Retrieve all amenities
GET	/amenities/<id>	Retrieve a specific amenity

📦 Example Request
Create a User
POST /api/v1/users
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@email.com"
}

🔍 Business Logic Features
Email format validation
Rating validation (1–5)
Latitude/Longitude validation
Relationship handling:
A Place has an owner (User)
A Review belongs to a User and a Place
Places can contain multiple Reviews
Data serialization with extended attributes for related objects

🧪 Testing the API
You can test the API using:
Postman
cURL
Browser (for GET routes)
Example:
curl http://127.0.0.1:5000/api/v1/users

🎯 Learning Objectives Achieved
Modular application design
RESTful API development with Flask
Implementation of the Facade pattern
Data validation and entity relationship handling
Clean architecture principles

🔮 Future Improvements (Part 3)
JWT Authentication
Role-based access control
Persistent database integration (SQLAlchemy)
Deployment configuration

