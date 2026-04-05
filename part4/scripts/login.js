// login.js
const loginForm = document.getElementById('login-form');
const errorMessage = document.getElementById('error-message');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorMessage.style.display = 'none';

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            // Task 2: Store JWT in cookie
            setCookie('token', data.access_token, 1);
            window.location.href = 'index.html';
        } else {
            const error = await response.json();
            errorMessage.innerText = error.msg || error.error || 'Login failed';
            errorMessage.style.display = 'block';
        }
    } catch (err) {
        errorMessage.innerText = 'Network error or server down';
        errorMessage.style.display = 'block';
    }
});
