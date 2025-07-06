-- HBnB Database CRUD Operations Test Script
-- Tests all basic database operations and constraints

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- =============================================================================
-- READ OPERATIONS - Verify initial data
-- =============================================================================

-- Test 1: Verify admin user exists
SELECT 'TEST 1: Admin user verification' as test_name;
SELECT 
    id,
    first_name,
    last_name,
    email,
    is_admin
FROM users 
WHERE email = 'admin@hbnb.io';

-- Test 2: Verify amenities exist
SELECT 'TEST 2: Initial amenities verification' as test_name;
SELECT id, name FROM amenities ORDER BY name;

-- =============================================================================
-- CREATE OPERATIONS - Test data insertion
-- =============================================================================

-- Test 3: Insert a regular user
SELECT 'TEST 3: Insert regular user' as test_name;
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
) VALUES (
    'user-test-uuid-123456789012345678901',
    'John',
    'Doe',
    'john.doe@example.com',
    '$2b$12$hashedpasswordexampleforjohndoe123',
    FALSE
);

-- Verify user was created
SELECT id, first_name, last_name, email, is_admin 
FROM users 
WHERE email = 'john.doe@example.com';

-- Test 4: Insert a place
SELECT 'TEST 4: Insert place with owner relationship' as test_name;
INSERT INTO places (
    id,
    title,
    description,
    price,
    latitude,
    longitude,
    owner_id
) VALUES (
    'place-test-uuid-123456789012345678901',
    'Beautiful Beach House',
    'A lovely house right on the beach with stunning ocean views.',
    299.99,
    25.7617,
    -80.1918,
    'user-test-uuid-123456789012345678901'
);

-- Verify place was created with owner relationship
SELECT 
    p.id,
    p.title,
    p.price,
    p.owner_id,
    u.first_name || ' ' || u.last_name as owner_name
FROM places p
JOIN users u ON p.owner_id = u.id
WHERE p.title = 'Beautiful Beach House';

-- Test 5: Insert place-amenity relationships
SELECT 'TEST 5: Insert many-to-many relationships' as test_name;
INSERT INTO place_amenity (place_id, amenity_id) VALUES 
    ('place-test-uuid-123456789012345678901', '550e8400-e29b-41d4-a716-446655440001'), -- WiFi
    ('place-test-uuid-123456789012345678901', '550e8400-e29b-41d4-a716-446655440002'); -- Swimming Pool

-- Verify many-to-many relationship
SELECT 
    p.title as place_title,
    a.name as amenity_name
FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE p.title = 'Beautiful Beach House';

-- Test 6: Insert a review
SELECT 'TEST 6: Insert review with constraints' as test_name;
INSERT INTO reviews (
    id,
    text,
    rating,
    user_id,
    place_id
) VALUES (
    'review-test-uuid-123456789012345678901',
    'Amazing place! The beach view was incredible and the amenities were perfect.',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1', -- Admin user reviewing
    'place-test-uuid-123456789012345678901'
);

-- Verify review with relationships
SELECT 
    r.text,
    r.rating,
    u.first_name || ' ' || u.last_name as reviewer_name,
    p.title as place_title
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id
WHERE r.text LIKE '%Amazing place%';

-- =============================================================================
-- UPDATE OPERATIONS - Test data modification
-- =============================================================================

-- Test 7: Update user information
SELECT 'TEST 7: Update user information' as test_name;
UPDATE users 
SET first_name = 'Jonathan', last_name = 'Smith'
WHERE email = 'john.doe@example.com';

-- Verify update
SELECT first_name, last_name, email 
FROM users 
WHERE email = 'john.doe@example.com';

-- Test 8: Update place price
SELECT 'TEST 8: Update place price' as test_name;
UPDATE places 
SET price = 349.99, description = 'Premium beach house with exclusive amenities.'
WHERE title = 'Beautiful Beach House';

-- Verify update
SELECT title, price, description 
FROM places 
WHERE title = 'Beautiful Beach House';

-- Test 9: Update review rating
SELECT 'TEST 9: Update review rating' as test_name;
UPDATE reviews 
SET rating = 4, text = 'Great place! Minor issues but overall excellent experience.'
WHERE text LIKE '%Amazing place%';

-- Verify update
SELECT text, rating 
FROM reviews 
WHERE text LIKE '%Great place%';

-- =============================================================================
-- CONSTRAINT TESTS - Verify data integrity
-- =============================================================================

-- Test 10: Test unique email constraint
SELECT 'TEST 10: Testing unique email constraint (should fail)' as test_name;
-- This should fail due to unique constraint
INSERT OR IGNORE INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
) VALUES (
    'user-duplicate-uuid-123456789012345678',
    'Jane',
    'Doe',
    'john.doe@example.com', -- Duplicate email
    '$2b$12$hashedpasswordexampleforjanedoe123',
    FALSE
);

-- Check that only one user exists with this email
SELECT COUNT(*) as user_count 
FROM users 
WHERE email = 'john.doe@example.com';

-- Test 11: Test rating constraint
SELECT 'TEST 11: Testing rating constraint (1-5 range)' as test_name;
-- This should fail due to rating constraint
INSERT OR IGNORE INTO reviews (
    id,
    text,
    rating,
    user_id,
    place_id
) VALUES (
    'review-invalid-rating-uuid-12345678901',
    'Invalid rating test',
    6, -- Invalid rating (should be 1-5)
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'place-test-uuid-123456789012345678901'
);

-- Test 12: Test unique user-place review constraint
SELECT 'TEST 12: Testing unique user-place review constraint (should fail)' as test_name;
-- This should fail - user already reviewed this place
INSERT OR IGNORE INTO reviews (
    id,
    text,
    rating,
    user_id,
    place_id
) VALUES (
    'review-duplicate-uuid-123456789012345678',
    'Another review for same place by same user',
    3,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1', -- Same user
    'place-test-uuid-123456789012345678901'  -- Same place
);

-- Verify only one review exists for this user-place combination
SELECT COUNT(*) as review_count
FROM reviews 
WHERE user_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1' 
AND place_id = 'place-test-uuid-123456789012345678901';

-- =============================================================================
-- COMPLEX QUERIES - Test relationships and joins
-- =============================================================================

-- Test 13: Complex query with all relationships
SELECT 'TEST 13: Complex query with all relationships' as test_name;
SELECT 
    p.title as place_title,
    p.price,
    owner.first_name || ' ' || owner.last_name as owner_name,
    GROUP_CONCAT(a.name, ', ') as amenities,
    AVG(r.rating) as average_rating,
    COUNT(r.id) as review_count
FROM places p
LEFT JOIN users owner ON p.owner_id = owner.id
LEFT JOIN place_amenity pa ON p.id = pa.place_id
LEFT JOIN amenities a ON pa.amenity_id = a.id
LEFT JOIN reviews r ON p.id = r.place_id
GROUP BY p.id, p.title, p.price, owner.first_name, owner.last_name;

-- =============================================================================
-- DELETE OPERATIONS - Test cascading deletes
-- =============================================================================

-- Test 14: Test cascade delete (delete user should delete their places and reviews)
SELECT 'TEST 14: Before cascade delete - count records' as test_name;
SELECT 
    (SELECT COUNT(*) FROM users WHERE email = 'john.doe@example.com') as users,
    (SELECT COUNT(*) FROM places WHERE owner_id = 'user-test-uuid-123456789012345678901') as places,
    (SELECT COUNT(*) FROM reviews WHERE user_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1') as reviews,
    (SELECT COUNT(*) FROM place_amenity WHERE place_id = 'place-test-uuid-123456789012345678901') as place_amenities;

-- Delete the test user (should cascade to places and their amenities)
DELETE FROM users WHERE email = 'john.doe@example.com';

SELECT 'TEST 14: After cascade delete - count records' as test_name;
SELECT 
    (SELECT COUNT(*) FROM users WHERE email = 'john.doe@example.com') as users,
    (SELECT COUNT(*) FROM places WHERE owner_id = 'user-test-uuid-123456789012345678901') as places,
    (SELECT COUNT(*) FROM reviews WHERE user_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1') as reviews,
    (SELECT COUNT(*) FROM place_amenity WHERE place_id = 'place-test-uuid-123456789012345678901') as place_amenities;

-- =============================================================================
-- FINAL VERIFICATION
-- =============================================================================

-- Test 15: Final state verification
SELECT 'TEST 15: Final database state' as test_name;
SELECT 'Users:' as table_name, COUNT(*) as record_count FROM users
UNION ALL
SELECT 'Places:', COUNT(*) FROM places  
UNION ALL
SELECT 'Reviews:', COUNT(*) FROM reviews
UNION ALL
SELECT 'Amenities:', COUNT(*) FROM amenities
UNION ALL
SELECT 'Place_Amenities:', COUNT(*) FROM place_amenity;

-- Show remaining data
SELECT 'Remaining users:' as info;
SELECT first_name, last_name, email, is_admin FROM users;

SELECT 'Remaining amenities:' as info;
SELECT name FROM amenities ORDER BY name;

SELECT 'All CRUD tests completed successfully!' as result;