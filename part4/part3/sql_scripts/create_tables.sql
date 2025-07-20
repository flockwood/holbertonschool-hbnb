-- HBnB Database Schema Creation Script
-- Creates all tables with proper relationships and constraints

-- Enable foreign key constraints (SQLite specific)
PRAGMA foreign_keys = ON;

-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- Create Users table
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX idx_users_email ON users(email);

-- Create Amenities table
CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create index on amenity name for faster lookups
CREATE INDEX idx_amenities_name ON amenities(name);

-- Create Places table
CREATE TABLE places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    latitude FLOAT NOT NULL CHECK (latitude >= -90 AND latitude <= 90),
    longitude FLOAT NOT NULL CHECK (longitude >= -180 AND longitude <= 180),
    owner_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    CONSTRAINT fk_places_owner 
        FOREIGN KEY (owner_id) 
        REFERENCES users(id) 
        ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_places_owner_id ON places(owner_id);
CREATE INDEX idx_places_price ON places(price);
CREATE INDEX idx_places_location ON places(latitude, longitude);

-- Create Reviews table
CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    CONSTRAINT fk_reviews_user 
        FOREIGN KEY (user_id) 
        REFERENCES users(id) 
        ON DELETE CASCADE,
    
    CONSTRAINT fk_reviews_place 
        FOREIGN KEY (place_id) 
        REFERENCES places(id) 
        ON DELETE CASCADE,
    
    -- Unique constraint: one review per user per place
    CONSTRAINT unique_user_place_review 
        UNIQUE (user_id, place_id)
);

-- Create indexes for better performance
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);

-- Create Place_Amenity junction table (Many-to-Many relationship)
CREATE TABLE place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Composite primary key
    PRIMARY KEY (place_id, amenity_id),
    
    -- Foreign key constraints
    CONSTRAINT fk_place_amenity_place 
        FOREIGN KEY (place_id) 
        REFERENCES places(id) 
        ON DELETE CASCADE,
    
    CONSTRAINT fk_place_amenity_amenity 
        FOREIGN KEY (amenity_id) 
        REFERENCES amenities(id) 
        ON DELETE CASCADE
);

-- Create indexes for junction table
CREATE INDEX idx_place_amenity_place_id ON place_amenity(place_id);
CREATE INDEX idx_place_amenity_amenity_id ON place_amenity(amenity_id);

-- Create triggers to update the updated_at timestamp automatically
-- Users table trigger
CREATE TRIGGER update_users_updated_at 
    AFTER UPDATE ON users
    FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Places table trigger
CREATE TRIGGER update_places_updated_at 
    AFTER UPDATE ON places
    FOR EACH ROW
BEGIN
    UPDATE places SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Reviews table trigger
CREATE TRIGGER update_reviews_updated_at 
    AFTER UPDATE ON reviews
    FOR EACH ROW
BEGIN
    UPDATE reviews SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Amenities table trigger
CREATE TRIGGER update_amenities_updated_at 
    AFTER UPDATE ON amenities
    FOR EACH ROW
BEGIN
    UPDATE amenities SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Display success message
SELECT 'Database schema created successfully!' as result;