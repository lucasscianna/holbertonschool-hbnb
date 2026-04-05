// review.js
const urlParams = new URLSearchParams(window.location.search);
const placeId = urlParams.get('id');

const reviewForm = document.getElementById('review-form');
const placeNameDisplay = document.getElementById('place-name-display');

document.addEventListener('DOMContentLoaded', () => {
    // Task 5: Form accessible only to authenticated users
    if (!getCookie('token')) {
        window.location.href = 'index.html';
        return;
    }

    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    fetchPlaceName();
    
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
                window.location.href = `place.html?id=${placeId}`;
            } else {
                const error = await response.json();
                alert(error.error || 'Failed to submit review');
            }
        } catch (err) {
            alert('Error connecting to the server');
        }
    });
});

async function fetchPlaceName() {
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`);
        const place = await response.json();
        placeNameDisplay.innerText = place.title;
    } catch (err) {
        placeNameDisplay.innerText = 'Place';
    }
}
