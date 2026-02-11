```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: POST /users
API->>BusinessLogic: validate user data

alt invalid user data
    BusinessLogic-->>API: validation error
    API-->>User: 400 Bad Request
else valid user data
    BusinessLogic->>Database: save user
    Database-->>BusinessLogic: user saved
    BusinessLogic-->>API: success
    API-->>User: 201 Created
end
```
User Registration Sequence

This diagram illustrates the user registration process.

The Business Logic layer validates the input data. If the data is invalid, an error response is returned.

If the data is valid, the user is persisted in the database and a success response is sent.