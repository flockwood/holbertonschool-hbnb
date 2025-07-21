document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = '/api/v1';
    let authToken = localStorage.getItem('token');
    
    // Check authentication status and update UI
    function updateAuthUI() {
        const loginButton = document.querySelector('.login-button');
        if (authToken && loginButton) {
            loginButton.textContent = 'Logout';
            loginButton.href = '#';
            loginButton.addEventListener('click', (e) => {
                e.preventDefault();
                logout();
            });
        }
    }
    
    // Logout function
    function logout() {
        localStorage.removeItem('token');
        authToken = null;
        alert('Logged out successfully');
        window.location.href = 'index.html';
    }
    
    // Get query parameters
    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }
    
    // Check which page we're on and load appropriate content
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    switch(currentPage) {
        case 'index.html':
        case '':
            loadPlaces();
            break;
        case 'place.html':
            const placeId = getQueryParam('id');
            if (placeId) {
                loadPlaceDetails(placeId);
            }
            break;
        case 'add_review.html':
            const reviewPlaceId = getQueryParam('place_id');
            if (reviewPlaceId) {
                loadPlaceForReview(reviewPlaceId);
            }
            break;
    }
    
    // Update authentication UI on all pages
    updateAuthUI();
    
    // Function to load all places
    async function loadPlaces() {
        try {
            const response = await fetch(`${API_BASE_URL}/places/`);
            if (response.ok) {
                const places = await response.json();
                displayPlaces(places);
            } else {
                console.error('Failed to load places');
            }
        } catch (error) {
            console.error('Error loading places:', error);
        }
    }
    
    // Function to display places
    function displayPlaces(places) {
        const placesList = document.getElementById('places-list');
        if (!placesList) return;
        
        if (places.length === 0) {
            placesList.innerHTML = '<p style="text-align: center; grid-column: 1/-1;">No places available yet.</p>';
            return;
        }
        
        placesList.innerHTML = places.map(place => `
            <article class="place-card">
                <h2>${place.title || 'Unnamed Place'}</h2>
                <p class="price">$${place.price || '0'} per night</p>
                <p class="location">Lat: ${place.latitude || 'N/A'}, Long: ${place.longitude || 'N/A'}</p>
                <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">
                    View Details
                </button>
            </article>
        `).join('');
    }
    
    // Handle login form submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch(`${API_BASE_URL}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    localStorage.setItem('token', data.access_token);
                    authToken = data.access_token;
                    alert('Login successful!');
                    window.location.href = 'index.html';
                } else {
                    const error = await response.json();
                    alert(error.error || 'Login failed. Please check your credentials.');
                }
            } catch (error) {
                console.error('Login error:', error);
                alert('An error occurred during login.');
            }
        });
    }
});