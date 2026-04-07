// index.js

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
});

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
    }
    // Always fetch places
    fetchPlaces(token);
}

async function fetchPlaces(token) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${API_BASE_URL}/places/`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
            setupPriceFilter(places);
        } else {
            console.warn('API returned error, using hardcoded data.');
            displayPlaces(HARDCODED_PLACES);
            setupPriceFilter(HARDCODED_PLACES);
        }
    } catch (err) {
        console.warn('API unavailable, using hardcoded data.', err);
        displayPlaces(HARDCODED_PLACES);
        setupPriceFilter(HARDCODED_PLACES);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = ''; // Clear current content

    if (places.length === 0) {
        placesList.innerHTML = '<p>No places found within this price range.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.innerHTML = `
            <h3>${place.title}</h3>
            <p class="price">$${place.price} per night</p>
            <p>Location: ${place.country || 'Unknown'}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(card);
    });
}

function setupPriceFilter(places) {
    const priceFilter = document.getElementById('price-filter');
    
    priceFilter.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        
        if (selectedPrice === 'All') {
            displayPlaces(places);
        } else {
            const maxPrice = parseFloat(selectedPrice);
            const filteredPlaces = places.filter(place => place.price <= maxPrice);
            displayPlaces(filteredPlaces);
        }
    });
}
