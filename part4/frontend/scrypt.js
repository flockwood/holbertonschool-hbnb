document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = '/api/v1';
    
    // Check if we're on the index page
    if (document.getElementById('places-list')) {
        loadPlaces();
    }
    
    // Function to load places
    async function loadPlaces() {
        try {
            const response = await fetch(`${API_BASE_URL}/places/`);
            if (response.ok) {
                const places = await response.json();
                displayPlaces(places);
            }
        } catch (error) {
            console.error('Error loading places:', error);
        }
    }
    
    // Function to display places
    function displayPlaces(places) {
        const placesList = document.getElementById('places-list');
        if (places.length === 0) {
            placesList.innerHTML = '<p>No places available yet.</p>';
            return;
        }
        
        placesList.innerHTML = places.map(place => `
            <article class="place-card">
                <h2>${place.title}</h2>
                <p class="price">$${place.price || 'N/A'} per night</p>
                <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">
                    View Details
                </button>
            </article>
        `).join('');
    }
    
    // Handle login form
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
                    alert('Login successful!');
                    window.location.href = 'index.html';
                } else {
                    alert('Login failed. Please check your credentials.');
                }
            } catch (error) {
                console.error('Login error:', error);
                alert('An error occurred during login.');
            }
        });
    }
});