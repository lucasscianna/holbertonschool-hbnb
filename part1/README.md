HBnB Evolution – Technical Documentation

📌 Project Overview
This document provides the technical foundation for the HBnB Evolution application, a simplified AirBnB-like platform.
The objective of this phase is to define:
The overall system architecture
The detailed business logic design
The interactions between system components
The data flow between application layers
This documentation will serve as a blueprint for the implementation phases of the project.

🏗️ 1. Architecture Overview
HBnB Evolution follows a three-layered architecture, ensuring separation of concerns and scalability.

🔹 1.1 Architecture Layers

1️⃣ Presentation Layer
Exposes services and API endpoints.
Handles user interactions.
Receives requests and returns responses.
Delegates business logic operations to the Business Layer.

2️⃣ Business Logic Layer
Contains the core domain models:
User
Place
Review
Amenity
Implements application rules.
Validates data.
Manages relationships between entities.

3️⃣ Persistence Layer
Responsible for data storage and retrieval.
Communicates with the database.
Abstracts database operations from business logic.

🔹 1.2 Communication Flow
The system uses a Facade Pattern between the Presentation Layer and the Business Logic Layer.
Flow:
Client → API (Presentation) → Facade → Business Logic → Persistence → Database
This ensures:
Loose coupling between layers
Clear separation of responsibilities
Easier maintenance and testing

📦 2. Business Logic Layer Design
The Business Logic Layer contains the domain entities and their rules.

👤 2.1 User Entity
Attributes
id (unique identifier)
first_name
last_name
email
password
is_admin (boolean)
created_at
updated_at
Responsibilities
Register new users
Update profile information
Delete users
Identify administrators
Business Rules
Email must be unique
Password must be stored securely
Only administrators may have elevated privileges

🏠 2.2 Place Entity
Attributes
id
title
description
price
latitude
longitude
owner (User)
amenities (List of Amenity)
created_at
updated_at
Responsibilities
Create new place listings
Update place details
Delete places
Retrieve place listings
Business Rules
A place must have an owner
Price must be a positive value
Latitude and longitude must be valid geographic coordinates

⭐ 2.3 Review Entity
Attributes
id
rating
comment
user (User)
place (Place)
created_at
updated_at
Responsibilities
Create reviews
Update reviews
Delete reviews
List reviews by place
Business Rules
A review must be linked to one user and one place
Rating must be within an acceptable range (e.g., 1–5)
A user can only review places they have visited (implementation-defined rule)

🛎️ 2.4 Amenity Entity
Attributes
id
name
description
created_at
updated_at
Responsibilities
Create amenities
Update amenities
Delete amenities
List available amenities
Business Rules
Amenity names should be unique
Amenities can be associated with multiple places

🔗 3. Relationships Between Entities
A User can own multiple Places.
A Place belongs to one User (owner).
A Place can have multiple Amenities.
An Amenity can belong to multiple Places.
A Review is associated with:
One User
One Place
A Place can have multiple Reviews.

🔁 4. API Interaction Scenarios
The following interactions demonstrate how data flows through the layers.

🔹 4.1 User Registration
Client sends registration request.
Presentation Layer validates request format.
Facade forwards request to Business Logic.
Business Logic:
Validates email uniqueness.
Hashes password.
Persistence Layer stores user in database.
Response returned to client.

🔹 4.2 Place Creation
Authenticated user submits place details.
Presentation Layer validates input.
Business Logic:
Confirms user exists.
Validates price and coordinates.
Persistence Layer saves place.
Success response returned.

🔹 4.3 Review Submission
User submits rating and comment.
Business Logic:
Confirms place exists.
Validates rating range.
Persistence Layer saves review.
Confirmation returned.

🔹 4.4 Fetching Places
Client requests list of places.
Presentation Layer forwards request.
Business Logic retrieves data.
Persistence Layer queries database.
List returned as API response.

🗄️ 5. Persistence Strategy
All entities are stored in a database.
Each entity:
Has a unique identifier.
Tracks created_at and updated_at timestamps.
The database implementation will be defined in Part 3 of the project.

📋 6. Constraints and Compliance
This documentation:
Clearly represents the three-layer architecture.
Reflects all specified business rules.
Defines all entity relationships.
Describes data flow between layers.
Provides sufficient detail to guide implementation.

🎯 Expected Outcome
This technical documentation provides:
A structured architectural blueprint.
A detailed business model definition.
A clear representation of system interactions.
A foundation for implementation in future project phases.
