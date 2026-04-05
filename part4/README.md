# HBnB Simple Web Client - Part 4

This project is a simple web client for the HBnB application, developed using HTML5, CSS3, and JavaScript ES6. It connects to the Flask-based API developed in the previous parts of the project.

## Project Structure

```text
part4/
├── hbnb/               # Backend Flask API (modified for CORS and country filtering)
├── index.html          # Main page (Places list)
├── login.html          # Login form
├── place.html          # Place details page
├── add_review.html     # Dedicated add review form
├── styles.css          # Global styles with rich aesthetics
├── scripts.js          # Shared JavaScript utilities
├── scripts/            # Modular JavaScript files
│   ├── index.js        # Places fetching and country filtering
│   ├── login.js        # Authentication logic
│   ├── place.js        # Place details and reviews loading
│   └── review.js       # Add review logic for dedicated page
└── images/             # Assets (Logo, Favicon)
```

## Features

- **Responsive Design**: A modern, premium interface inspired by top vacation rental platforms.
- **Authentication**: Secure login using JWT stored in cookies.
- **Dynamic Content**: Data fetched asynchronously from the API.
- **Country Filtering**: Client-side filtering of places by country.
- **Review System**: Authenticated users can submit reviews for places.
- **CORS Support**: API modified to allow requests from the web client.

## Setup Instructions

### 1. Start the API
Navigate to the `hbnb` directory and start the Flask server:
```bash
cd hbnb
pip install -r requirements.txt
python run.py
```
*Note: Ensure you have `flask-cors` installed.*

### 2. Open the Client
Open `index.html` in your favorite web browser.

## Technologies Used

- **Frontend**: HTML5, Vanilla CSS3, JavaScript ES6 (Fetch API).
- **Backend Integration**: AJAX/Fetch, Cookies for session management.
- **Dev Tools**: Python (Flask) for the API.

---
*Created by Antigravity for the Holberton School HBnB Project.*
