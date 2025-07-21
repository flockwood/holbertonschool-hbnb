-- HBnB Initial Data Insertion Script
-- Inserts administrator user and initial amenities

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Insert Administrator User
-- Password hash for 'admin1234' using bcrypt
-- Generated using: python -c "import bcrypt; print(bcrypt.hashpw(b'admin1234', bcrypt.gensalt()).decode())"
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin,
    created_at,
    updated_at
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxkUJqyqdG2mlHyaNgdMQ9dOQgO',  -- admin1234 hashed
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert Initial Amenities with generated UUIDs
INSERT INTO amenities (
    id,
    name,
    created_at,
    updated_at
) VALUES 
(
    '550e8400-e29b-41d4-a716-446655440001',
    'WiFi',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),
(
    '550e8400-e29b-41d4-a716-446655440002',
    'Swimming Pool',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),
(
    '550e8400-e29b-41d4-a716-446655440003',
    'Air Conditioning',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Verify the data was inserted correctly
SELECT 'Initial data insertion completed!' as result;

-- Display inserted admin user (without password)
SELECT 
    id,
    first_name,
    last_name,
    email,
    is_admin,
    created_at
FROM users 
WHERE email = 'admin@hbnb.io';

-- Display inserted amenities
SELECT 
    id,
    name,
    created_at
FROM amenities 
ORDER BY name;