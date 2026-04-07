// review.js

function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review-text').value;
            const reviewRating = document.getElementById('review-rating').value;
            submitReview(token, placeId, reviewText, reviewRating);
        });
    }
});

async function submitReview(token, placeId, reviewText, reviewRating) {
    try {
        const response = await fetch(`${API_BASE_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: parseInt(reviewRating)
            })
        });
        handleResponse(response);
    } catch (err) {
        alert('Failed to submit review due to a network error.');
    }
}

async function handleResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        document.getElementById('review-form').reset();
        // Redirect back to the place details
        window.location.href = `place.html?id=${getPlaceIdFromURL()}`;
    } else {
        const errorData = await response.json().catch(() => ({}));
        alert(`Failed to submit review: ${errorData.error || response.statusText}`);
    }
}
