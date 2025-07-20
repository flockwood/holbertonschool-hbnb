#!/usr/bin/env python3
"""
Generate Password Hash Script
Creates bcrypt hash for admin password and generates UUIDs.
"""

import bcrypt
import uuid

def generate_password_hash(password):
    """Generate bcrypt hash for a password."""
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def generate_uuids(count=5):
    """Generate multiple UUIDs."""
    return [str(uuid.uuid4()) for _ in range(count)]

def verify_password(password, hashed):
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def main():
    """Generate and display password hashes and UUIDs."""
    print("🔐 PASSWORD HASH GENERATOR")
    print("=" * 50)
    
    # Generate hash for admin password
    admin_password = "admin1234"
    admin_hash = generate_password_hash(admin_password)
    
    print(f"Admin Password: {admin_password}")
    print(f"Admin Hash: {admin_hash}")
    
    # Verify the hash works
    verification = verify_password(admin_password, admin_hash)
    print(f"Hash Verification: {'✅ Success' if verification else '❌ Failed'}")
    
    print("\n" + "=" * 50)
    print("🆔 UUID GENERATOR")
    print("=" * 50)
    
    # Fixed admin UUID as specified in requirements
    admin_uuid = "36c9050e-ddd3-4c3b-9731-9f487208bbc1"
    print(f"Admin User UUID (fixed): {admin_uuid}")
    
    # Generate amenity UUIDs
    print("\nAmenity UUIDs:")
    amenity_names = ["WiFi", "Swimming Pool", "Air Conditioning"]
    amenity_uuids = [
        "550e8400-e29b-41d4-a716-446655440001",
        "550e8400-e29b-41d4-a716-446655440002", 
        "550e8400-e29b-41d4-a716-446655440003"
    ]
    
    for name, uuid_val in zip(amenity_names, amenity_uuids):
        print(f"  {name}: {uuid_val}")
    
    print("\n" + "=" * 50)
    print("📝 SQL READY VALUES")
    print("=" * 50)
    
    print("Admin user INSERT statement:")
    print(f"""
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
) VALUES (
    '{admin_uuid}',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '{admin_hash}',
    TRUE
);""")
    
    print("\nAmenities INSERT statements:")
    for i, (name, uuid_val) in enumerate(zip(amenity_names, amenity_uuids)):
        print(f"""
INSERT INTO amenities (id, name) VALUES (
    '{uuid_val}',
    '{name}'
);""")
    
    print("\n" + "=" * 50)
    print("🧪 ADDITIONAL TEST UUIDS")
    print("=" * 50)
    
    # Generate some additional UUIDs for testing
    test_uuids = generate_uuids(5)
    test_purposes = [
        "Test User 1",
        "Test User 2", 
        "Test Place 1",
        "Test Place 2",
        "Test Review 1"
    ]
    
    for purpose, uuid_val in zip(test_purposes, test_uuids):
        print(f"  {purpose}: {uuid_val}")

if __name__ == "__main__":
    main()