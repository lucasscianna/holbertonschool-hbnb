// Common utilities for HBnB web client

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// ============================================================
// HARDCODED DATA - Works without API / database
// ============================================================
const HARDCODED_PLACES = [
    {
        id: 'place-1',
        title: 'Cozy Parisian Studio',
        description: 'Lovely studio in the heart of Paris, close to the Eiffel Tower.',
        price: 85,
        latitude: 48.8584,
        longitude: 2.2945,
        country: 'France',
        owner: { first_name: 'Alice', last_name: 'Host' },
        amenities: [
            { id: 'am-1', name: 'WiFi' },
            { id: 'am-2', name: 'Air Conditioning' },
            { id: 'am-3', name: 'Kitchen' }
        ],
        reviews: [
            { user_name: 'John D.', rating: 5, text: 'Amazing place, perfect location near the Eiffel Tower! The studio was clean and cozy.' },
            { user_name: 'Marie L.', rating: 4, text: 'Great stay overall. The kitchen was well equipped. Would come back!' }
        ]
    },
    {
        id: 'place-2',
        title: 'Luxury Villa in Bali',
        description: 'Breathtaking villa with a private pool and rice terrace views.',
        price: 250,
        latitude: -8.4095,
        longitude: 115.1889,
        country: 'Indonesia',
        owner: { first_name: 'Admin', last_name: 'System' },
        amenities: [
            { id: 'am-1', name: 'WiFi' },
            { id: 'am-4', name: 'Pool' },
            { id: 'am-2', name: 'Air Conditioning' },
            { id: 'am-5', name: 'Free Parking' }
        ],
        reviews: [
            { user_name: 'Sophie R.', rating: 5, text: 'Absolutely stunning! The private pool overlooking the rice terraces was unforgettable.' },
            { user_name: 'Lucas M.', rating: 5, text: 'Best villa experience ever. The staff was incredibly helpful.' },
            { user_name: 'Emma W.', rating: 4, text: 'Beautiful property. A bit far from the town center but worth it for the views.' }
        ]
    },
    {
        id: 'place-3',
        title: 'Modern Loft in New York',
        description: 'Spacious loft in Brooklyn with a stunning city skyline view.',
        price: 150,
        latitude: 40.7128,
        longitude: -74.0060,
        country: 'United States',
        owner: { first_name: 'Alice', last_name: 'Host' },
        amenities: [
            { id: 'am-1', name: 'WiFi' },
            { id: 'am-6', name: 'TV' },
            { id: 'am-7', name: 'Heating' },
            { id: 'am-8', name: 'Washer' }
        ],
        reviews: [
            { user_name: 'David K.', rating: 4, text: 'Great loft with an incredible view of the skyline. Very spacious and clean.' }
        ]
    }
];

/**
 * Find a hardcoded place by its ID.
 */
function getHardcodedPlaceById(id) {
    return HARDCODED_PLACES.find(p => p.id === id) || HARDCODED_PLACES[0];
}


// LocalStorage Management (used instead of cookies to avoid file:// security errors)
function setCookie(name, value, days) {
    localStorage.setItem(name, value);
}

function getCookie(name) {
    return localStorage.getItem(name);
}

function eraseCookie(name) {
    localStorage.removeItem(name);
}

// Authentication check
function checkAuth() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const navLinks = document.getElementById('nav-links');

    if (token) {
        // User is logged in
        if (loginLink) {
            loginLink.innerText = 'Log Out';
            loginLink.href = '#';
            loginLink.classList.remove('login-button');
            loginLink.style.cursor = 'pointer';
            loginLink.addEventListener('click', (e) => {
                e.preventDefault();
                logoutUser();
            });
        }
        return true;
    }
    return false;
}

function logoutUser() {
    eraseCookie('token');
    window.location.href = 'index.html';
}

// Redirect if not authenticated (Task 3 & 5 requirement)
function requireAuth() {
    if (!checkAuth()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Format API errors
async function handleResponse(response) {
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Something went wrong');
    }
    return response.json();
}

// UI elements will pull functions from here when needed.

// Initialize authentication check on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});

/**
 * Returns an SVG icon string for a given amenity name.
 * Falls back to a generic star icon for unrecognized amenities.
 */
function getAmenityIcon(name) {
    const n = name.toLowerCase().trim();

    const icons = {
        'wifi': '<svg viewBox="0 0 24 24"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><circle cx="12" cy="20" r="1" fill="currentColor" stroke="none"/></svg>',

        'pool': '<svg viewBox="0 0 24 24"><path d="M2 20c2-1 4-1 6 0s4 1 6 0 4-1 6 0"/><path d="M2 16c2-1 4-1 6 0s4 1 6 0 4-1 6 0"/><path d="M9 6a3 3 0 1 0 0-6"/><path d="M9 12V6"/><path d="M15 12V6"/></svg>',

        'air conditioning': '<svg viewBox="0 0 24 24"><path d="M8 16a4 4 0 1 0 8 0"/><path d="M12 2v10"/><path d="M5.2 7.8L12 12"/><path d="M18.8 7.8L12 12"/></svg>',

        'kitchen': '<svg viewBox="0 0 24 24"><path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3zm0 0v7"/></svg>',

        'tv': '<svg viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="15" rx="2" ry="2"/><polyline points="17 2 12 7 7 2"/></svg>',

        'parking': '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/></svg>',

        'washer': '<svg viewBox="0 0 24 24"><rect x="3" y="1" width="18" height="22" rx="2"/><circle cx="12" cy="13" r="5"/><circle cx="12" cy="13" r="2"/><path d="M7 5h2"/><circle cx="16" cy="5" r="1" fill="currentColor" stroke="none"/></svg>',

        'dryer': '<svg viewBox="0 0 24 24"><rect x="3" y="1" width="18" height="22" rx="2"/><circle cx="12" cy="13" r="5"/><path d="M9 13c0-1 1-2 3-2s3 1 3 2"/><path d="M7 5h2"/><circle cx="16" cy="5" r="1" fill="currentColor" stroke="none"/></svg>',

        'heating': '<svg viewBox="0 0 24 24"><path d="M12 2a5 5 0 0 0-5 5c0 4 5 8 5 12a5 5 0 0 0 5-5c0-4-5-8-5-12z"/><path d="M12 14a2 2 0 0 0-2 2c0 1.5 2 3 2 4a2 2 0 0 0 2-2c0-1.5-2-3-2-4z"/></svg>',

        'iron': '<svg viewBox="0 0 24 24"><path d="M21 17H3a2 2 0 0 1 0-4h12a4 4 0 0 1 4 4h2z"/><path d="M6 13V7a4 4 0 0 1 4-4h0"/><line x1="3" y1="21" x2="21" y2="21"/></svg>',

        'hot tub': '<svg viewBox="0 0 24 24"><path d="M9 6c0-1 1-2 2-2s2 1 2 2"/><path d="M5 6c0-1 1-2 2-2s2 1 2 2"/><path d="M13 6c0-1 1-2 2-2s2 1 2 2"/><path d="M2 12h20"/><path d="M4 12v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-6"/></svg>',

        'gym': '<svg viewBox="0 0 24 24"><path d="M6.5 6.5a2 2 0 0 1 3 0L12 9l2.5-2.5a2 2 0 0 1 3 0"/><path d="M4 12h16"/><path d="M2 10h2v4H2z"/><path d="M20 10h2v4h-2z"/><path d="M6 8h2v8H6z"/><path d="M16 8h2v8h-2z"/></svg>',

        'elevator': '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 3v18"/><polyline points="8 9 6 7 4 9"/><polyline points="20 15 18 17 16 15"/></svg>',

        'pets allowed': '<svg viewBox="0 0 24 24"><circle cx="11" cy="4" r="2"/><circle cx="18" cy="8" r="2"/><circle cx="20" cy="15" r="2"/><path d="M9 10a5 5 0 0 1 5 5c0 2-2 3-5 3s-5-1-5-3a5 5 0 0 1 5-5z"/></svg>',

        'breakfast': '<svg viewBox="0 0 24 24"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>',
    };

    // Try exact match first, then partial match
    if (icons[n]) return icons[n];

    for (const key in icons) {
        if (n.includes(key) || key.includes(n)) {
            return icons[key];
        }
    }

    // Fallback: generic amenity icon (check/star)
    return '<svg viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>';
}
