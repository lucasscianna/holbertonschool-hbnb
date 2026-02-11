```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: POST /places
API->>BusinessLogic: validate place data

alt invalid place data
    BusinessLogic-->>API: validation error
    API-->>User: 400 Bad Request
else valid place data
    BusinessLogic->>Database: save place
    Database-->>BusinessLogic: place saved
    BusinessLogic-->>API: success
    API-->>User: 201 Created
end
```
Place Creation Sequence

This sequence diagram shows how a new place is created.

Invalid input data is rejected by the Business Logic layer.

Valid place data is saved in the database and confirmed to the user.