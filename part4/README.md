# HBnB Evolution - Part 4 🏠

A full-stack AirBnB-like application with a modern web interface, built with Flask backend and vanilla JavaScript frontend, featuring JWT authentication, real-time place listings, and a comprehensive review system.

## 📋 Overview

HBnB Evolution Part 4 adds a complete web interface to the existing backend, enabling users to:
- Browse and filter property listings
- View detailed place information with amenities
- Submit authenticated reviews with ratings
- Manage user sessions with secure JWT tokens
- Experience a responsive, modern UI design

## 🆕 Part 4 Features

### Frontend Interface
- **Responsive Design**: Mobile-friendly layout that adapts to all screen sizes
- **Modern UI/UX**: Clean, intuitive interface with smooth interactions
- **Dynamic Content**: Real-time data loading without page refreshes
- **Cookie-based Auth**: Secure JWT token storage in cookies

### Key Pages
1. **Home Page (`index.html`)**
   - Grid layout of all available places
   - Price filtering with dropdown
   - Quick access to place details
   - Dynamic login/logout button

2. **Place Details (`place.html`)**
   - Complete place information
   - Owner details and amenities list
   - Reviews section with ratings
   - Inline review submission form (authenticated users only)

3. **Login Page (`login.html`)**
   - Secure authentication form
   - JWT token generation
   - Automatic redirect after login

4. **Review Form (`add_review.html`)**
   - Dedicated review submission page
   - Place information display
   - Rating selection (1-5 stars)
   - Authentication protection

## 🏗️ Architecture

```
part4/
├── frontend/                    # Static web interface
│   ├── index.html              # Home page with places grid
│   ├── place.html              # Individual place details
│   ├── login.html              # User authentication
│   ├── add_review.html         # Review submission form
│   ├── styles.css              # Responsive CSS styling
│   ├── scripts.js              # Frontend JavaScript logic
│   └── images/                 # Logo and icons
│       ├── logo.png           
│       └── icon.png           
├── app/                        # Flask backend
│   ├── __init__.py            # App factory with CORS
│   ├── api/v1/                # RESTful API endpoints
│   │   ├── auth.py            # JWT authentication
│   │   ├── users.py           # User management
│   │   ├── places.py          # Place operations
│   │   ├── reviews.py         # Review system
│   │   └── amenities.py       # Amenity management
│   ├── models/                # SQLAlchemy models
│   ├── persistence/           # Data access layer
│   └── services/              # Business logic
├── scripts/                   # Utility scripts
├── tests/                     # Test suites
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
└── run.py                     # Application entry point
```

## 🚀 Features

### Authentication & Security
- **JWT Token Authentication**: Secure token-based auth system
- **Cookie Storage**: Tokens stored in httpOnly cookies
- **Protected Routes**: Authentication required for reviews
- **Role-Based Access**: Admin privileges for user/amenity management
- **Password Hashing**: Bcrypt encryption for passwords

### Review System
- **Authenticated Submission**: Only logged-in users can review
- **Business Rules Enforcement**:
  - Users cannot review their own places
  - One review per user per place
  - Rating validation (1-5 stars)
- **Real-time Updates**: Reviews appear immediately after submission
- **Error Handling**: Clear messages for all error cases

### Place Management
- **Dynamic Listing**: Real-time place grid with details
- **Price Filtering**: Filter places by maximum price
- **Detailed Views**: Complete information with amenities
- **Owner Information**: Display host details
- **Relationship Loading**: Automatic loading of related data

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Loading States**: Visual feedback during data fetching
- **Error Messages**: User-friendly error notifications
- **Success Confirmations**: Clear success feedback
- **Automatic Redirects**: Smart navigation after actions

## 🔧 Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Setup Steps

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/hbnb-evolution.git
cd hbnb-evolution/part4
```

2. **Create Virtual Environment**
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize Database**
```bash
python scripts/migration_script.py
# or
python scripts/init_db.py
```

5. **Run the Application**
```bash
python run.py
```

6. **Access the Application**
- Frontend: http://127.0.0.1:5000/
- API Docs: http://127.0.0.1:5000/api/v1/doc/

### Default Credentials
- **Admin User**
  - Email: `admin@hbnb.com`
  - Password: `admin123`

## 🧪 Testing

### Quick System Check
```bash
python tests/quick_system_check.py
```

### Comprehensive Test Suite
```bash
python tests/comprehensive_test_suite.py
```

### Test Review Feature
```bash
# Create test data
python test_review_setup.py

# Run automated tests
python test_review_functionality.py

# Check results
python check_reviews.py
```

### Manual Testing Steps

1. **Test Authentication**
   - Go to login page
   - Login with credentials
   - Verify logout functionality

2. **Test Place Browsing**
   - View all places on home page
   - Test price filtering
   - Click place for details

3. **Test Review Submission**
   - Login as user
   - Navigate to a place (not owned by you)
   - Submit a review with rating
   - Verify review appears

4. **Test Error Cases**
   - Try to review without login (should redirect)
   - Try to review your own place (should show error)
   - Try to review same place twice (should show error)

## 🔗 API Endpoints

All backend endpoints remain available:

### Authentication
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/protected` - Verify token

### Places
- `GET /api/v1/places/` - List all places (public)
- `GET /api/v1/places/{id}` - Get place details (public)
- `POST /api/v1/places/` - Create place (auth required)
- `PUT /api/v1/places/{id}` - Update place (owner only)

### Reviews
- `GET /api/v1/reviews/` - List all reviews
- `POST /api/v1/reviews/` - Submit review (auth required)
- `GET /api/v1/reviews/places/{place_id}/reviews` - Get place reviews
- `PUT /api/v1/reviews/{id}` - Update review (author only)
- `DELETE /api/v1/reviews/{id}` - Delete review (author only)

### Users & Amenities
- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user (admin only)
- `GET /api/v1/amenities/` - List amenities
- `POST /api/v1/amenities/` - Create amenity (admin only)

## 📱 Frontend Features

### Dynamic Content Loading
```javascript
// Places are loaded dynamically
fetchPlaces();

// Reviews load when viewing place details
fetchPlaceReviews(placeId);

// Real-time filtering
filterPlacesByPrice(maxPrice);
```

### Authentication State Management
```javascript
// Token stored in cookies
setCookie('token', data.access_token, 1);

// Auth check on protected pages
checkAuthentication();

// Dynamic UI updates based on auth state
updateAuthUI();
```

### Error Handling
```javascript
// Comprehensive error handling
handleReviewResponse(response, placeId);

// User-friendly error messages
alert(`Failed to submit review: ${error.message}`);
```

## 🎨 UI/UX Features

### Responsive Design
- Mobile-first approach
- Flexible grid layouts
- Touch-friendly buttons
- Optimized for all screen sizes

### Visual Feedback
- Hover effects on interactive elements
- Clear success/error messages
- Loading states for async operations
- Smooth transitions

### Accessibility
- Semantic HTML structure
- Proper form labels
- Keyboard navigation support
- Clear error messages

## 🛡️ Security Features

1. **JWT Authentication**
   - Secure token generation
   - Token expiration (24 hours)
   - Bearer token in headers

2. **Input Validation**
   - Frontend form validation
   - Backend data validation
   - SQL injection prevention

3. **CORS Configuration**
   - Enabled for frontend-backend communication
   - Proper origin handling

4. **Password Security**
   - Bcrypt hashing
   - Never exposed in responses
   - Secure transmission

## 🚦 Business Rules

1. **Review Restrictions**
   - Must be authenticated to review
   - Cannot review own property
   - One review per user per place
   - Rating must be 1-5

2. **Access Control**
   - Public: View places, reviews
   - Authenticated: Create places, submit reviews
   - Owner only: Update/delete own content
   - Admin only: Manage users and amenities

## 🔮 Future Enhancements

- **User Registration**: Self-service account creation
- **Image Upload**: Property photos with cloud storage
- **Advanced Search**: Filter by location, amenities, dates
- **Booking System**: Reservation management
- **Payment Integration**: Secure payment processing
- **Real-time Updates**: WebSocket for live notifications
- **Mobile App**: Native iOS/Android applications

## 📈 Performance Optimizations

- **Lazy Loading**: Load content as needed
- **Caching Strategy**: Browser caching for static assets
- **Minification**: Compress CSS/JS for production
- **API Optimization**: Efficient queries and pagination
- **CDN Integration**: Serve static files from CDN

## 🐛 Troubleshooting

### Common Issues

1. **"Not enough segments" Error**
   - Clear cookies and login again
   - Check token format in browser console

2. **Review Form Not Showing**
   - Verify you're logged in
   - Check browser console for errors

3. **Places Not Loading**
   - Ensure backend server is running
   - Check network tab for API errors

4. **Cannot Submit Review**
   - Verify you're not reviewing own place
   - Check if you've already reviewed
   - Ensure all fields are filled

### Debug Commands

```javascript
// Check authentication status
console.log('Token:', getCookie('token'));

// Verify current user
fetch('/api/v1/auth/protected', {
    headers: { 'Authorization': `Bearer ${getCookie('token')}` }
}).then(r => r.json()).then(console.log);

// Check place ownership
const placeId = new URLSearchParams(window.location.search).get('id');
fetch(`/api/v1/places/${placeId}`).then(r => r.json()).then(console.log);
```

## 📄 License

This project is part of the Holberton School curriculum.

## 👥 Author

- **Fernando Lockwood** - Full Stack Development
- GitHub: [@flockwood](https://github.com/flockwood)

