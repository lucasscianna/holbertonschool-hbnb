// place.js
const urlParams = new URLSearchParams(window.location.search);
const placeId = urlParams.get('id');

const placeTitle = document.getElementById('place-title');
const placeHost = document.getElementById('place-host');
const placePrice = document.getElementById('place-price');
const placeDescription = document.getElementById('place-description');
const amenitiesList = document.getElementById('amenities-list');
const reviewsList = document.getElementById('reviews-list');
const addReviewSection = document.getElementById('add-review-section');
const reviewForm = document.getElementById('review-form');

document.addEventListener('DOMContentLoaded', () => {
    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    fetchPlaceDetails();
    
    // Task 4: Provide access to the add review form if the user is authenticated
    if (getCookie('token')) {
        addReviewSection.style.display = 'block';
        setupReviewForm();
    }
});

async function fetchPlaceDetails() {
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`);
        const place = await response.json();

        placeTitle.innerText = place.title;
        placeHost.innerText = `Host: ${place.owner.first_name} ${place.owner.last_name || ''}`;
        placePrice.innerText = `$${place.price} per night`;
        placeDescription.innerText = place.description || 'No description available.';

        // Populate amenities
        amenitiesList.innerHTML = '';
        place.amenities.forEach(amenity => {
            const tag = document.createElement('span');
            tag.className = 'amenity-tag';
            tag.innerText = amenity.name;
            amenitiesList.appendChild(tag);
        });

        // Populate reviews
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

    } catch (err) {
        placeTitle.innerText = 'Error loading place details.';
    }
}

function setupReviewForm() {
    reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = document.getElementById('review-text').value;
        const rating = parseInt(document.getElementById('review-rating').value);

        try {
            const response = await fetch(`${API_BASE_URL}/reviews/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('token')}`
                },
                body: JSON.stringify({
                    place_id: placeId,
                    text: text,
                    rating: rating
                })
            });

            if (response.ok) {
                // Refresh reviews
                fetchPlaceDetails();
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
