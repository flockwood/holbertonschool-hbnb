document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = '/api/v1';
    
    // Cookie helper functions
    function setCookie(name, value, days = 1) {
        const expires = new Date();
        expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
        document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
    }
    
    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }
    
    function deleteCookie(name) {
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
    }
    
    // Get token from cookie instead of localStorage
    let authToken = getCookie('token');
    
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
        deleteCookie('token');
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
    
    // Function to load place details
    async function loadPlaceDetails(placeId) {
        try {
            const response = await fetch(`${API_BASE_URL}/places/${placeId}`);
            if (response.ok) {
                const place = await response.json();
                displayPlaceDetails(place);
                loadPlaceReviews(placeId);
            } else {
                console.error('Failed to load place details');
            }
        } catch (error) {
            console.error('Error loading place details:', error);
        }
    }
    
    // Function to display place details
    function displayPlaceDetails(place) {
        const placeDetails = document.getElementById('place-details');
        if (!placeDetails) return;
        
        placeDetails.innerHTML = `
            <div class="place-info">
                <h1>${place.title || 'Unnamed Place'}</h1>
                <p class="host-info">Hosted by ${place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : 'Unknown'}</p>
                <p class="price">$${place.price || '0'} per night</p>
                <div class="description">
                    <h2>Description</h2>
                    <p>${place.description || 'No description available.'}</p>
                </div>
                <div class="amenities">
                    <h2>Amenities</h2>
                    <ul>
                        ${place.amenities && place.amenities.length > 0 
                            ? place.amenities.map(amenity => `<li>${amenity.name}</li>`).join('')
                            : '<li>No amenities listed</li>'
                        }
                    </ul>
                </div>
            </div>
        `;
        
        // Update the add review link
        const addReviewSection = document.getElementById('add-review');
        if (addReviewSection && authToken) {
            const reviewLink = addReviewSection.querySelector('a[href="add_review.html"]');
            if (reviewLink) {
                reviewLink.href = `add_review.html?place_id=${place.id}`;
            }
        }
    }
    
    // Function to load reviews for a place
    async function loadPlaceReviews(placeId) {
        try {
            const response = await fetch(`${API_BASE_URL}/reviews/places/${placeId}/reviews`);
            if (response.ok) {
                const reviews = await response.json();
                displayReviews(reviews);
            }
        } catch (error) {
            console.error('Error loading reviews:', error);
        }
    }
    
    // Function to display reviews
    function displayReviews(reviews) {
        const reviewsContainer = document.querySelector('.reviews-container');
        if (!reviewsContainer) return;
        
        if (reviews.length === 0) {
            reviewsContainer.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
            return;
        }
        
        reviewsContainer.innerHTML = reviews.map(review => `
            <article class="review-card">
                <div class="review-header">
                    <strong>User ${review.user_id ? review.user_id.substring(0, 8) : 'Anonymous'}</strong>
                    <span class="rating">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</span>
                </div>
                <p>${review.text || review.comment || 'No comment'}</p>
            </article>
        `).join('');
    }
    
    // Function to load place info for review page
    async function loadPlaceForReview(placeId) {
        try {
            const response = await fetch(`${API_BASE_URL}/places/${placeId}`);
            if (response.ok) {
                const place = await response.json();
                displayPlaceForReview(place);
            }
        } catch (error) {
            console.error('Error loading place for review:', error);
        }
    }
    
    // Function to display place info on review page
    function displayPlaceForReview(place) {
        const placeIdentifier = document.querySelector('.place-identifier');
        if (placeIdentifier) {
            placeIdentifier.innerHTML = `
                <h2>Reviewing: ${place.title || 'Unnamed Place'}</h2>
                <p class="place-summary">
                    Hosted by ${place.owner ? `${place.owner.first_name} ${place.owner.last_name}` : 'Unknown'} 
                    • $${place.price || '0'} per night
                </p>
            `;
        }
    }
    
    // Handle login form submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
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
                    // Store JWT token in cookie as required
                    setCookie('token', data.access_token, 1); // 1 day expiration
                    authToken = data.access_token;
                    alert('Login successful!');
                    window.location.href = 'index.html';
                } else {
                    const error = await response.json();
                    alert('Login failed: ' + (error.error || error.message || response.statusText));
                }
            } catch (error) {
                console.error('Login error:', error);
                alert('An error occurred during login. Please try again.');
            }
        });
    }
    
    // Handle review form submission
    const reviewForm = document.getElementById('review-form');
    if (reviewForm && currentPage === 'add_review.html') {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!authToken) {
                alert('Please login to submit a review');
                window.location.href = 'login.html';
                return;
            }
            
            const placeId = getQueryParam('place_id');
            const reviewText = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;
            
            try {
                const response = await fetch(`${API_BASE_URL}/reviews/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authToken}`
                    },
                    body: JSON.stringify({
                        text: reviewText,
                        rating: parseInt(rating),
                        place_id: placeId
                    })
                });
                
                if (response.ok) {
                    alert('Review submitted successfully!');
                    window.location.href = `place.html?id=${placeId}`;
                } else {
                    const error = await response.json();
                    alert(error.message || 'Failed to submit review');
                }
            } catch (error) {
                console.error('Review submission error:', error);
                alert('An error occurred while submitting the review.');
            }
        });
    }
    
    // Handle place detail page review form
    if (reviewForm && currentPage === 'place.html') {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (!authToken) {
                alert('Please login to submit a review');
                window.location.href = 'login.html';
                return;
            }
            
            const placeId = getQueryParam('id');
            const reviewText = document.getElementById('review-text').value;
            const rating = document.getElementById('rating').value;
            
            try {
                const response = await fetch(`${API_BASE_URL}/reviews/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${authToken}`
                    },
                    body: JSON.stringify({
                        text: reviewText,
                        rating: parseInt(rating),
                        place_id: placeId
                    })
                });
                
                if (response.ok) {
                    alert('Review submitted successfully!');
                    location.reload(); // Reload to show new review
                } else {
                    const error = await response.json();
                    alert(error.message || 'Failed to submit review');
                }
            } catch (error) {
                console.error('Review submission error:', error);
                alert('An error occurred while submitting the review.');
            }
        });
    }
    
    // Handle price filter
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', async (e) => {
            const maxPrice = e.target.value;
            try {
                const response = await fetch(`${API_BASE_URL}/places/`);
                if (response.ok) {
                    let places = await response.json();
                    
                    // Filter places by price if a max price is selected
                    if (maxPrice) {
                        places = places.filter(place => place.price <= parseInt(maxPrice));
                    }
                    
                    displayPlaces(places);
                }
            } catch (error) {
                console.error('Error filtering places:', error);
            }
        });
    }
});