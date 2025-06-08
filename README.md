# HBnB Evolution 🏠

A simplified AirBnB-like application built with a clean three-layer architecture, allowing users to manage property listings, reviews, and amenities.

## 📋 Overview

HBnB Evolution is a property rental platform that enables users to:
- List and manage properties
- Search for places with various filters
- Write and read reviews
- Manage property amenities

## 🏗️ Architecture

The application follows a **three-layer architecture**:

```
┌─────────────────────────┐
│   Presentation Layer    │
│      (ServiceAPI)       │
└───────────┬─────────────┘
            │
┌───────────▼─────────────┐
│  Business Logic Layer   │
│   (HBnBFacade + Models) │
└───────────┬─────────────┘
            │
┌───────────▼─────────────┐
│   Persistence Layer     │
│    (DAOs + Database)    │
└─────────────────────────┘
```

### Key Components

- **ServiceAPI**: Handles HTTP requests and responses
- **HBnBFacade**: Orchestrates business logic and coordinates between entities
- **Models**: Core entities (User, Place, Review, Amenity)
- **DAOs**: Data Access Objects for database operations

## 🚀 Features

### User Management
- User registration with email validation
- Profile management
- Authentication and authorization
- Admin user support

### Place Management
- Create, update, and delete property listings
- Add location details (coordinates)
- Set pricing
- Associate multiple amenities

### Review System
- Submit reviews with ratings (1-5) and comments
- One review per user per place
- Users cannot review their own properties

### Amenity Management
- Create and manage amenities (WiFi, Pool, etc.)
- Many-to-many relationship with places

## 📊 Data Models

### User
```
- id (UUID)
- first_name
- last_name
- email (unique)
- password (hashed)
- is_admin
- created_at
- updated_at
```

### Place
```
- id (UUID)
- title
- description
- price
- latitude
- longitude
- owner (User)
- amenities (List<Amenity>)
- created_at
- updated_at
```

### Review
```
- id (UUID)
- rating (1-5)
- comment
- user (User)
- place (Place)
- created_at
- updated_at
```

### Amenity
```
- id (UUID)
- name
- description
- created_at
- updated_at
```

## 🔗 API Endpoints

### Users
- `POST /api/users/register` - Register new user
- `GET /api/users/{id}` - Get user details
- `PUT /api/users/{id}` - Update user profile
- `DELETE /api/users/{id}` - Delete user

### Places
- `POST /api/places` - Create new place (authenticated)
- `GET /api/places` - List places with filters
- `GET /api/places/{id}` - Get place details
- `PUT /api/places/{id}` - Update place (owner only)
- `DELETE /api/places/{id}` - Delete place (owner only)

### Reviews
- `POST /api/places/{place_id}/reviews` - Submit review (authenticated)
- `GET /api/places/{place_id}/reviews` - Get reviews for place
- `PUT /api/reviews/{id}` - Update review (author only)
- `DELETE /api/reviews/{id}` - Delete review (author only)

### Amenities
- `GET /api/amenities` - List all amenities
- `POST /api/amenities` - Create amenity (admin only)
- `PUT /api/amenities/{id}` - Update amenity (admin only)
- `DELETE /api/amenities/{id}` - Delete amenity (admin only)

## 🛡️ Business Rules

1. **Email Uniqueness**: Each email can only be registered once
2. **Review Restrictions**: 
   - Users cannot review their own places
   - One review per user per place
3. **Authentication Required**: Place creation and review submission require authentication
4. **Owner Permissions**: Only place owners can update/delete their listings
5. **Admin Privileges**: Only admins can manage amenities

## 🚦 HTTP Status Codes

- `200 OK` - Successful GET request
- `201 Created` - Resource successfully created
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Conflict with existing data

## 📝 Technical Documentation

For detailed technical documentation, including:
- UML Class Diagrams
- Sequence Diagrams
- Package Diagrams

Please refer to the `/docs` directory.

## 🔧 Setup & Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/hbnb-evolution.git

# Navigate to project directory
cd hbnb-evolution

# Install dependencies
[Installation commands based on your tech stack]

# Set up database
[Database setup commands]

# Run the application
[Run commands]
```

## 🧪 Testing

```bash
# Run unit tests
[Test command]

# Run integration tests
[Test command]
```

## 📄 License

This project is part of the HBnB Evolution educational project.

## 👤 Author

**Fernando Lockwood**

---

**Note**: This is a simplified clone of AirBnB created for educational purposes.
