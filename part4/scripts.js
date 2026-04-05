// Common utilities for HBnB web client

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

// Cookie Management
function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function eraseCookie(name) {
    document.cookie = name + '=; Max-Age=-99999999;';
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

// Initialize common UI elements
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});
