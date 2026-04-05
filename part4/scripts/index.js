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
        // Fetch places data if the user is authenticated
        fetchPlaces(token);
    }
}

async function fetchPlaces(token) {
    try {
        const response = await fetch(`${API_BASE_URL}/places`, {
            method: 'GET',
            headers: {
                // Include the token in the Authorization header
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
            setupPriceFilter(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (err) {
        console.error('Error fetching places:', err);
        document.getElementById('places-list').innerHTML = '<p style="color: red;">Error loading places. Ensure API is running.</p>';
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
