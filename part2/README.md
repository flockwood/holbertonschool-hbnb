# HBnB Evolution 🏠

A production-ready AirBnB-like REST API built with Flask and Flask-RESTX, featuring a clean three-layer architecture for managing property rentals, user accounts, reviews, and amenities.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.0+-green.svg)
![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)
![Tests](https://img.shields.io/badge/tests-46%2F46%20passing-brightgreen.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Business Logic](#business-logic)
- [Contributing](#contributing)
- [Author](#author)

## 🌟 Overview

HBnB Evolution is a comprehensive property rental platform API that enables users to:

- **Manage Properties**: Create, update, and search property listings
- **User Management**: Register users with secure authentication
- **Review System**: Submit and manage property reviews with ratings
- **Amenity Management**: Organize and categorize property features
- **RESTful API**: Full CRUD operations with proper HTTP status codes

## ✨ Features

### 🔐 User Management
- User registration with email validation
- Secure password hashing using bcrypt
- Profile management and updates
- Admin user support for enhanced permissions

### 🏡 Property Management
- Create and manage property listings
- Geographic coordinates with validation
- Pricing management
- Multi-amenity support with many-to-many relationships

### ⭐ Review System
- Rating system (1-5 stars)
- Text reviews with validation
- One review per user per property
- Users cannot review their own properties

### 🛠️ Amenity Management
- Create and categorize amenities (WiFi, Pool, Parking, etc.)
- Associate multiple amenities with properties
- Admin-only amenity management

### 🔧 Technical Features
- **RESTful API Design**: Follows REST principles
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Proper HTTP status codes and error messages
- **Auto Documentation**: Interactive Swagger UI documentation
- **Clean Architecture**: Three-layer separation of concerns

## 🏗️ Architecture

The application follows a **three-layer architecture** pattern:

```
┌─────────────────────────────────┐
│     Presentation Layer          │
│       (Flask-RESTX API)         │
│  • Endpoints & Request Handling │
│  • Input Validation             │
│  • Response Formatting          │
└─────────────┬───────────────────┘
              │
┌─────────────▼───────────────────┐
│     Business Logic Layer        │
│      (HBnBFacade + Models)      │
│  • Business Rules               │
│  • Data Validation              │
│  • Entity Relationships         │
└─────────────┬───────────────────┘
              │
┌─────────────▼───────────────────┐
│     Persistence Layer           │
│   (Repository + InMemory DB)    │
│  • Data Storage                 │
│  • CRUD Operations              │
│  • Data Retrieval               │
└─────────────────────────────────┘
```

### Key Components

- **API Endpoints**: Handle HTTP requests and responses
- **HBnBFacade**: Orchestrates business logic and coordinates entities
- **Models**: Core entities (User, Place, Review, Amenity) with validation
- **Repository**: Data access layer with in-memory storage

## 🚀 API Endpoints

### Users
| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| POST | `/api/v1/users/` | Register new user | 201, 400, 409 |
| GET | `/api/v1/users/` | List all users | 200 |
| GET | `/api/v1/users/{id}` | Get user details | 200, 404 |
| PUT | `/api/v1/users/{id}` | Update user profile | 200, 400, 404, 409 |

### Places
| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| POST | `/api/v1/places/` | Create new place | 201, 400, 404 |
| GET | `/api/v1/places/` | List all places | 200 |
| GET | `/api/v1/places/{id}` | Get place details | 200, 404 |
| PUT | `/api/v1/places/{id}` | Update place | 200, 400, 404 |

### Reviews
| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| POST | `/api/v1/reviews/` | Create new review | 201, 400, 404 |
| GET | `/api/v1/reviews/` | List all reviews | 200 |
| GET | `/api/v1/reviews/{id}` | Get review details | 200, 404 |
| PUT | `/api/v1/reviews/{id}` | Update review | 200, 400, 404 |
| DELETE | `/api/v1/reviews/{id}` | Delete review | 200, 404 |
| GET | `/api/v1/reviews/places/{place_id}/reviews` | Get reviews for place | 200, 404 |

### Amenities
| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| POST | `/api/v1/amenities/` | Create new amenity | 201, 400, 409 |
| GET | `/api/v1/amenities/` | List all amenities | 200 |
| GET | `/api/v1/amenities/{id}` | Get amenity details | 200, 404 |
| PUT | `/api/v1/amenities/{id}` | Update amenity | 200, 400, 404, 409 |

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hbnb-evolution.git
   cd hbnb-evolution/part2
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Access the API**
   - API Base URL: `http://localhost:5000/api/v1/`
   - Interactive Documentation: `http://localhost:5000/api/v1/`

## 💻 Usage

### Quick Start Example

1. **Create a User**
   ```bash
   curl -X POST "http://localhost:5000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "John",
       "last_name": "Doe",
       "email": "john@example.com",
       "password": "securepassword"
     }'
   ```

2. **Create a Place**
   ```bash
   curl -X POST "http://localhost:5000/api/v1/places/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Cozy Beach House",
       "description": "Beautiful oceanfront property",
       "price": 150.0,
       "latitude": 25.7617,
       "longitude": -80.1918,
       "owner_id": "user-id-from-step-1"
     }'
   ```

3. **Create a Review**
   ```bash
   curl -X POST "http://localhost:5000/api/v1/reviews/" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Amazing stay! Highly recommended.",
       "rating": 5,
       "user_id": "user-id-from-step-1",
       "place_id": "place-id-from-step-2"
     }'
   ```

### Interactive Testing

Visit `http://localhost:5000/api/v1/` to access the **Swagger UI** where you can:
- View all available endpoints
- Test API calls interactively
- See request/response examples
- View data models and validation rules

## 🧪 Testing

The project includes comprehensive testing with **100% success rate** across all endpoints.

### Run Tests

1. **Start the application**
   ```bash
   python run.py
   ```

2. **Run validation tests** (in a new terminal)
   ```bash
   pip install requests
   python tests/test_validation.py
   ```

3. **Run comprehensive tests**
   ```bash
   python tests/final_test_report.py
   ```

4. **Run individual test suites**
   ```bash
   # Test user functionality
   python tests/test_user.py
   
   # Test place functionality  
   python tests/test_places.py
   
   # Test review functionality
   python tests/test_reviews.py
   ```

### Test Coverage
- **46 total tests** - All passing ✅
- CRUD operations for all entities
- Input validation testing
- Error handling verification
- HTTP status code validation
- Edge case testing

### Test Categories
- ✅ **User Management**: Registration, validation, updates
- ✅ **Place Management**: Creation, coordinate validation, owner verification
- ✅ **Review System**: CRUD operations, rating validation, relationship checks
- ✅ **Amenity Management**: Creation, uniqueness validation
- ✅ **Error Handling**: 404 errors, validation failures, invalid data

## 📚 API Documentation

### Interactive Documentation
Access the auto-generated Swagger documentation at: `http://localhost:5000/api/v1/`

### Data Models

#### User Model
```json
{
  "id": "uuid",
  "first_name": "string",
  "last_name": "string", 
  "email": "string (email format)",
  "is_admin": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Place Model
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "price": "float (positive)",
  "latitude": "float (-90 to 90)",
  "longitude": "float (-180 to 180)",
  "owner_id": "uuid",
  "amenities": ["uuid"],
  "reviews": ["uuid"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Review Model
```json
{
  "id": "uuid",
  "text": "string",
  "rating": "integer (1-5)",
  "user_id": "uuid",
  "place_id": "uuid",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Amenity Model
```json
{
  "id": "uuid",
  "name": "string (unique)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 📁 Project Structure

```
part2/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py         # User endpoints
│   │       ├── places.py        # Place endpoints
│   │       ├── reviews.py       # Review endpoints
│   │       └── amenities.py     # Amenity endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # Base model with common attributes
│   │   ├── user.py             # User model with validation
│   │   ├── place.py            # Place model with coordinate validation
│   │   ├── review.py           # Review model with rating validation
│   │   └── amenity.py          # Amenity model
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py           # Business logic facade
│   └── persistence/
│       ├── __init__.py
│       └── repository.py       # Data access layer
├── tests/
│   ├── test_user.py            # User endpoint tests
│   ├── test_places.py          # Place endpoint tests
│   ├── test_reviews.py         # Review endpoint tests
│   ├── test_validation.py      # Input validation tests
│   ├── comprehensive_test.py   # Full functionality tests
│   └── final_test_report.py    # Complete test suite with reporting
├── requirements.txt             # Project dependencies
├── run.py                      # Application entry point
├── config.py                   # Configuration settings
└── README.md                   # This file
```

## 🎯 Business Logic

### Validation Rules

#### User Validation
- First name and last name are required
- Email must be valid format and unique
- Password is required and securely hashed

#### Place Validation
- Title is required
- Price must be positive number
- Latitude: -90 to 90 degrees
- Longitude: -180 to 180 degrees
- Owner must exist

#### Review Validation
- Text is required
- Rating must be between 1 and 5
- User and place must exist
- Users cannot review their own places

#### Amenity Validation
- Name is required and must be unique

### Relationships
- **User ↔ Place**: One-to-many (owner relationship)
- **User ↔ Review**: One-to-many (reviewer relationship)
- **Place ↔ Review**: One-to-many (place being reviewed)
- **Place ↔ Amenity**: Many-to-many (place features)


## 👤 Author

**Fernando Lockwood**
- Email: [flockwood@live.com]
- GitHub: [@flockwood]