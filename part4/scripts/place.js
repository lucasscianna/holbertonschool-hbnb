// place.js

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    setupReviewForm();
});

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

function checkAuthentication() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review-section');
    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    if (!token) {
        if (addReviewSection) addReviewSection.style.display = 'none';
        // Fetch public details
        fetchPlaceDetails(null, placeId);
    } else {
        if (addReviewSection) addReviewSection.style.display = 'block';
        // Store the token for later use and fetch details
        fetchPlaceDetails(token, placeId);
    }
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        // Ensure the request includes the JWT token for authentication if available
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
            document.getElementById('place-title').innerText = 'Error loading place details.';
        }
    } catch (err) {
        console.error('Error:', err);
        document.getElementById('place-title').innerText = 'Error connecting to server.';
    }
}

function displayPlaceDetails(place) {
    // Populate simple text elements
    document.getElementById('place-title').innerText = place.title || 'Unknown Place';
    document.getElementById('place-host').innerText = `Host: ${place.owner ? place.owner.first_name + ' ' + (place.owner.last_name || '') : 'Unknown'}`;
    document.getElementById('place-price').innerText = `$${place.price} per night`;
    document.getElementById('place-description').innerText = place.description || 'No description available.';

    // Populate amenities
    const amenitiesList = document.getElementById('amenities-list');
    amenitiesList.innerHTML = '';
    if (place.amenities && place.amenities.length > 0) {
        place.amenities.forEach(amenity => {
            const tag = document.createElement('span');
            tag.className = 'amenity-tag';
            tag.innerText = amenity.name;
            amenitiesList.appendChild(tag);
        });
    } else {
        amenitiesList.innerHTML = '<p>No amenities listed.</p>';
    }

    // Populate reviews
    const reviewsList = document.getElementById('reviews-list');
    reviewsList.innerHTML = '';
    if (place.reviews && place.reviews.length > 0) {
        place.reviews.forEach(review => {
            const card = document.createElement('div');
            card.className = 'review-card';
            card.innerHTML = `
                <p class="user-name">${review.user_name || 'Guest'}</p>
                <p class="rating">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
                <p>${review.text}</p>
            `;
            reviewsList.appendChild(card);
        });
    } else {
        reviewsList.innerHTML = '<p>No reviews yet.</p>';
    }
}

function setupReviewForm() {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;

    reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = document.getElementById('review-text').value;
        const rating = parseInt(document.getElementById('review-rating').value);
        const placeId = getPlaceIdFromURL();
        const token = getCookie('token');

        if (!token) return;

        try {
            const response = await fetch(`${API_BASE_URL}/reviews/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    place_id: placeId,
                    text: text,
                    rating: rating
                })
            });

            if (response.ok) {
                // Refresh place details to see the new review
                fetchPlaceDetails(token, placeId);
                reviewForm.reset();
                alert('Review added successfully!');
            } else {
                const error = await response.json();
                alert(error.error || 'Failed to submit review');
            }
        } catch (err) {
            alert('Error connecting to the server');
        }
    });
}
