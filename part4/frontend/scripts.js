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
    
    // Check authentication and control login link visibility
    function checkAuthentication() {
        const token = getCookie('token');
        const loginLink = document.getElementById('login-link');
        
        if (loginLink) {
            if (!token) {
                loginLink.style.display = 'inline-block';
            } else {
                loginLink.style.display = 'none';
            }
        }
        
        // Also update the .login-button in the nav
        updateAuthUI();
    }
    
    // Check authentication status and update UI
    function updateAuthUI() {
        const loginButton = document.querySelector('.login-button');
        if (authToken && loginButton) {
            loginButton.textContent = 'Logout';
            loginButton.href = '#';
            loginButton.style.display = 'inline-block';
            // Remove old event listeners and add new one
            const newButton = loginButton.cloneNode(true);
            loginButton.parentNode.replaceChild(newButton, loginButton);
            newButton.addEventListener('click', (e) => {
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
    
    // Get place ID from URL (alias for requirement compliance)
    function getPlaceIdFromURL() {
        return getQueryParam('id');
    }
    
    // Check authentication and control form visibility
    checkAuthentication();
    
    // Check which page we're on and load appropriate content
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    switch(currentPage) {
        case 'index.html':
        case '':
            // Always fetch places (authentication not required for viewing)
            fetchPlaces();
            setupPriceFilter();
            break;
        case 'place.html':
            const placeId = getPlaceIdFromURL();
            if (placeId) {
                // Check auth and show/hide review form
                const token = getCookie('token');
                const addReviewSection = document.getElementById('add-review');
                if (addReviewSection) {
                    if (!token) {
                        addReviewSection.style.display = 'none';
                    } else {
                        addReviewSection.style.display = 'block';
                    }
                }
                // Fetch place details (token is optional for viewing)
                fetchPlaceDetails(token, placeId);
            }
            break;
        case 'add_review.html':
            const reviewPlaceId = getQueryParam('place_id');
            if (reviewPlaceId) {
                loadPlaceForReview(reviewPlaceId);
            }
            break;
    }
    
    // Store places data globally for filtering
    let allPlaces = [];
    
    // Function to fetch places from API
    async function fetchPlaces() {
        try {
            const headers = {};
            // Include token if available (optional for viewing places)
            if (authToken) {
                headers['Authorization'] = `Bearer ${authToken}`;
            }
            
            const response = await fetch(`${API_BASE_URL}/places/`, {
                method: 'GET',
                headers: headers
            });
            
            if (response.ok) {
                const places = await response.json();
                allPlaces = places; // Store for filtering
                displayPlaces(places);
                setupPriceFilterOptions(places);
            } else {
                console.error('Failed to fetch places');
                displayPlaces([]);
            }
        } catch (error) {
            console.error('Error fetching places:', error);
            displayPlaces([]);
        }
    }
    
    // Function to display places
    function displayPlaces(places) {
        const placesList = document.getElementById('places-list');
        if (!placesList) return;
        
        // Clear current content
        placesList.innerHTML = '';
        
        if (places.length === 0) {
            placesList.innerHTML = '<p style="text-align: center; grid-column: 1/-1;">No places available.</p>';
            return;
        }
        
        // Create and append place elements
        places.forEach(place => {
            const placeElement = document.createElement('article');
            placeElement.className = 'place-card';
            placeElement.dataset.price = place.price || 0;
            
            placeElement.innerHTML = `
                <h2>${place.title || 'Unnamed Place'}</h2>
                <p class="price">${place.price || '0'} per night</p>
                <p class="location">Lat: ${place.latitude || 'N/A'}, Long: ${place.longitude || 'N/A'}</p>
                <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">
                    View Details
                </button>
            `;
            
            placesList.appendChild(placeElement);
        });
    }
    
    // Function to setup price filter options
    function setupPriceFilterOptions(places) {
        const priceFilter = document.getElementById('price-filter');
        if (!priceFilter) return;
        
        // Clear existing options
        priceFilter.innerHTML = '';
        
        // Add filter options as specified
        const filterOptions = [
            { value: '', text: 'All' },
            { value: '10', text: 'Up to $10' },
            { value: '50', text: 'Up to $50' },
            { value: '100', text: 'Up to $100' }
        ];
        
        filterOptions.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.text;
            priceFilter.appendChild(optionElement);
        });
    }
    
    // Function to setup price filter event listener
    function setupPriceFilter() {
        const priceFilter = document.getElementById('price-filter');
        if (!priceFilter) return;
        
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            filterPlacesByPrice(selectedPrice);
        });
    }
    
    // Function to filter places by price
    function filterPlacesByPrice(maxPrice) {
        const placeCards = document.querySelectorAll('.place-card');
        
        placeCards.forEach(card => {
            const placePrice = parseFloat(card.dataset.price) || 0;
            
            if (maxPrice === '' || placePrice <= parseFloat(maxPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    // Function to load all places (deprecated - use fetchPlaces instead)
    async function loadPlaces() {
        // Redirect to fetchPlaces for consistency
        await fetchPlaces();
    }
    
    // Function to fetch place details
    async function fetchPlaceDetails(token, placeId) {
        try {
            const headers = {};
            // Include token if available (optional for viewing places)
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
                // Fetch reviews separately
                fetchPlaceReviews(placeId);
            } else {
                console.error('Failed to fetch place details');
                document.getElementById('place-details').innerHTML = 
                    '<p class="error">Failed to load place details. Please try again.</p>';
            }
        } catch (error) {
            console.error('Error fetching place details:', error);
            document.getElementById('place-details').innerHTML = 
                '<p class="error">An error occurred while loading place details.</p>';
        }
    }
    
    // Function to display place details
    function displayPlaceDetails(place) {
        const placeDetails = document.getElementById('place-details');
        if (!placeDetails) return;
        
        // Clear current content
        placeDetails.innerHTML = '';
        
        // Create place info container
        const placeInfo = document.createElement('div');
        placeInfo.className = 'place-info';
        
        // Title
        const title = document.createElement('h1');
        title.textContent = place.title || 'Unnamed Place';
        placeInfo.appendChild(title);
        
        // Host info
        const hostInfo = document.createElement('p');
        hostInfo.className = 'host-info';
        hostInfo.textContent = place.owner ? 
            `Hosted by ${place.owner.first_name} ${place.owner.last_name}` : 
            'Hosted by Unknown';
        placeInfo.appendChild(hostInfo);
        
        // Price
        const price = document.createElement('p');
        price.className = 'price';
        price.textContent = `${place.price || '0'} per night`;
        placeInfo.appendChild(price);
        
        // Description
        const descriptionSection = document.createElement('div');
        descriptionSection.className = 'description';
        descriptionSection.innerHTML = `
            <h2>Description</h2>
            <p>${place.description || 'No description available.'}</p>
        `;
        placeInfo.appendChild(descriptionSection);
        
        // Amenities
        const amenitiesSection = document.createElement('div');
        amenitiesSection.className = 'amenities';
        const amenitiesTitle = document.createElement('h2');
        amenitiesTitle.textContent = 'Amenities';
        amenitiesSection.appendChild(amenitiesTitle);
        
        const amenitiesList = document.createElement('ul');
        if (place.amenities && place.amenities.length > 0) {
            place.amenities.forEach(amenity => {
                const li = document.createElement('li');
                li.textContent = amenity.name;
                amenitiesList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'No amenities listed';
            amenitiesList.appendChild(li);
        }
        amenitiesSection.appendChild(amenitiesList);
        placeInfo.appendChild(amenitiesSection);
        
        // Append everything to place details
        placeDetails.appendChild(placeInfo);
        
        // Update the add review form link with place ID
        const addReviewSection = document.getElementById('add-review');
        if (addReviewSection && authToken) {
            const reviewLink = addReviewSection.querySelector('a[href="add_review.html"]');
            if (reviewLink) {
                reviewLink.href = `add_review.html?place_id=${place.id}`;
            }
        }
    }
    
    // Function to fetch reviews for a place
    async function fetchPlaceReviews(placeId) {
        try {
            const response = await fetch(`${API_BASE_URL}/reviews/places/${placeId}/reviews`);
            if (response.ok) {
                const reviews = await response.json();
                displayReviews(reviews);
            } else {
                console.error('Failed to fetch reviews');
            }
        } catch (error) {
            console.error('Error fetching reviews:', error);
        }
    }
    
    // Function to display reviews
    function displayReviews(reviews) {
        const reviewsContainer = document.querySelector('.reviews-container');
        if (!reviewsContainer) return;
        
        // Clear current content
        reviewsContainer.innerHTML = '';
        
        if (reviews.length === 0) {
            const noReviews = document.createElement('p');
            noReviews.textContent = 'No reviews yet. Be the first to review!';
            reviewsContainer.appendChild(noReviews);
            return;
        }
        
        // Create review cards
        reviews.forEach(review => {
            const reviewCard = document.createElement('article');
            reviewCard.className = 'review-card';
            
            const reviewHeader = document.createElement('div');
            reviewHeader.className = 'review-header';
            
            const userName = document.createElement('strong');
            userName.textContent = review.user_id ? 
                `User ${review.user_id.substring(0, 8)}` : 
                'Anonymous';
            reviewHeader.appendChild(userName);
            
            const rating = document.createElement('span');
            rating.className = 'rating';
            rating.textContent = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
            reviewHeader.appendChild(rating);
            
            reviewCard.appendChild(reviewHeader);
            
            const reviewText = document.createElement('p');
            reviewText.textContent = review.text || review.comment || 'No comment';
            reviewCard.appendChild(reviewText);
            
            reviewsContainer.appendChild(reviewCard);
        });
    }
    
    // Backward compatibility - keep old function names
    async function loadPlaceDetails(placeId) {
        const token = getCookie('token');
        await fetchPlaceDetails(token, placeId);
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
});