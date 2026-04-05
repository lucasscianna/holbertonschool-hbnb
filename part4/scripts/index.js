// index.js
const placesList = document.getElementById('places-list');
const countryFilter = document.getElementById('country-filter');

document.addEventListener('DOMContentLoaded', () => {
    // Task 3: Redirect to login if not authenticated
    if (!getCookie('token')) {
        window.location.href = 'login.html';
        return;
    }

    fetchPlaces();
});

async function fetchPlaces() {
    try {
        const response = await fetch(`${API_BASE_URL}/places`, {
            headers: {
                'Authorization': `Bearer ${getCookie('token')}`
            }
        });
        const places = await response.json();
        
        displayPlaces(places);
        populateCountries(places);
        
        countryFilter.addEventListener('change', () => {
            const selectedCountry = countryFilter.value;
            if (selectedCountry === 'All') {
                displayPlaces(places);
            } else {
                const filtered = places.filter(p => p.country === selectedCountry);
                displayPlaces(filtered);
            }
        });

    } catch (err) {
        placesList.innerHTML = '<p style="color: red;">Error loading places. Make sure the API is running.</p>';
    }
}

function displayPlaces(places) {
    placesList.innerHTML = '';
    
    if (places.length === 0) {
        placesList.innerHTML = '<p>No places found.</p>';
        return;
    }

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.innerHTML = `
            <h3>${place.title}</h3>
            <p class="price">$${place.price} per night</p>
            <p>Location: ${place.country}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesList.appendChild(card);
    });
}

function populateCountries(places) {
    const countries = [...new Set(places.map(p => p.country))].sort();
    
    // Clear existing options except "All"
    countryFilter.innerHTML = '<option value="All">All Countries</option>';
    
    countries.forEach(country => {
        if (country) {
            const option = document.createElement('option');
            option.value = country;
            option.innerText = country;
            countryFilter.appendChild(option);
        }
    });
}
