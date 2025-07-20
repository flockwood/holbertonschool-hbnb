#!/usr/bin/env python3
"""
Simple SQL Database Setup
Creates the HBnB database with embedded SQL commands.
"""

import sqlite3
import os

def create_database():
    """Create the complete HBnB database with embedded SQL."""
    
    db_file = "hbnb_raw_sql.db"
    
    # Remove existing database
    if os.path.exists(db_file):
        print(f"🗑️  Removing existing database: {db_file}")
        os.remove(db_file)
    
    # Connect to database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    print("🗄️  HBnB DATABASE SETUP")
    print("========================")
    print("✅ Database connection established")
    
    try:
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        print("\n📊 Creating database schema...")
        
        # Create Users table
        cursor.execute("""
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
        """)
        print("   ✅ Users table created")
        
        # Create Amenities table
        cursor.execute("""
            CREATE TABLE amenities (
                id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("   ✅ Amenities table created")
        
        # Create Places table
        cursor.execute("""
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
                FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        print("   ✅ Places table created")
        
        # Create Reviews table
        cursor.execute("""
            CREATE TABLE reviews (
                id CHAR(36) PRIMARY KEY,
                text TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                user_id CHAR(36) NOT NULL,
                place_id CHAR(36) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
                UNIQUE (user_id, place_id)
            );
        """)
        print("   ✅ Reviews table created")
        
        # Create Place_Amenity junction table
        cursor.execute("""
            CREATE TABLE place_amenity (
                place_id CHAR(36) NOT NULL,
                amenity_id CHAR(36) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (place_id, amenity_id),
                FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
                FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
            );
        """)
        print("   ✅ Place_Amenity junction table created")
        
        # Create indexes
        indexes = [
            "CREATE INDEX idx_users_email ON users(email);",
            "CREATE INDEX idx_places_owner_id ON places(owner_id);",
            "CREATE INDEX idx_reviews_user_id ON reviews(user_id);",
            "CREATE INDEX idx_reviews_place_id ON reviews(place_id);"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        print("   ✅ Indexes created")
        
        print("\n📝 Inserting initial data...")
        
        # Insert admin user
        cursor.execute("""
            INSERT INTO users (
                id, first_name, last_name, email, password, is_admin
            ) VALUES (
                '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
                'Admin',
                'HBnB',
                'admin@hbnb.io',
                '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxkUJqyqdG2mlHyaNgdMQ9dOQgO',
                TRUE
            );
        """)
        print("   ✅ Admin user created")
        
        # Insert amenities
        amenities_data = [
            ('550e8400-e29b-41d4-a716-446655440001', 'WiFi'),
            ('550e8400-e29b-41d4-a716-446655440002', 'Swimming Pool'),
            ('550e8400-e29b-41d4-a716-446655440003', 'Air Conditioning')
        ]
        
        for amenity_id, amenity_name in amenities_data:
            cursor.execute("""
                INSERT INTO amenities (id, name) VALUES (?, ?);
            """, (amenity_id, amenity_name))
        print("   ✅ Initial amenities created")
        
        print("\n🧪 Running basic tests...")
        
        # Test: Verify admin user
        cursor.execute("SELECT first_name, last_name, email, is_admin FROM users WHERE email = 'admin@hbnb.io';")
        admin = cursor.fetchone()
        if admin:
            print(f"   ✅ Admin user verified: {admin[0]} {admin[1]} ({admin[2]}) - Admin: {admin[3]}")
        else:
            print("   ❌ Admin user not found")
        
        # Test: Verify amenities
        cursor.execute("SELECT COUNT(*) FROM amenities;")
        amenity_count = cursor.fetchone()[0]
        print(f"   ✅ Amenities verified: {amenity_count} amenities created")
        
        # Test: Create test data
        print("\n🔧 Creating test data...")
        
        # Create test user
        cursor.execute("""
            INSERT INTO users (
                id, first_name, last_name, email, password, is_admin
            ) VALUES (
                'test-user-uuid-123456789012345678901',
                'John',
                'Doe',
                'john@test.com',
                '$2b$12$hashedpasswordexample123456789012',
                FALSE
            );
        """)
        print("   ✅ Test user created")
        
        # Create test place
        cursor.execute("""
            INSERT INTO places (
                id, title, description, price, latitude, longitude, owner_id
            ) VALUES (
                'test-place-uuid-12345678901234567890',
                'Test Beach House',
                'A beautiful test house for testing relationships.',
                199.99,
                25.7617,
                -80.1918,
                'test-user-uuid-123456789012345678901'
            );
        """)
        print("   ✅ Test place created")
        
        # Add amenities to place
        cursor.execute("""
            INSERT INTO place_amenity (place_id, amenity_id) VALUES 
            ('test-place-uuid-12345678901234567890', '550e8400-e29b-41d4-a716-446655440001'),
            ('test-place-uuid-12345678901234567890', '550e8400-e29b-41d4-a716-446655440002');
        """)
        print("   ✅ Place-amenity relationships created")
        
        # Create test review
        cursor.execute("""
            INSERT INTO reviews (
                id, text, rating, user_id, place_id
            ) VALUES (
                'test-review-uuid-1234567890123456789',
                'Great place for testing! All relationships work perfectly.',
                5,
                '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
                'test-place-uuid-12345678901234567890'
            );
        """)
        print("   ✅ Test review created")
        
        # Test complex query with relationships
        print("\n🔗 Testing relationships...")
        cursor.execute("""
            SELECT 
                p.title as place_title,
                p.price,
                owner.first_name || ' ' || owner.last_name as owner_name,
                GROUP_CONCAT(a.name, ', ') as amenities,
                AVG(r.rating) as avg_rating,
                COUNT(r.id) as review_count
            FROM places p
            LEFT JOIN users owner ON p.owner_id = owner.id
            LEFT JOIN place_amenity pa ON p.id = pa.place_id
            LEFT JOIN amenities a ON pa.amenity_id = a.id
            LEFT JOIN reviews r ON p.id = r.place_id
            WHERE p.title = 'Test Beach House'
            GROUP BY p.id, p.title, p.price, owner.first_name, owner.last_name;
        """)
        
        result = cursor.fetchone()
        if result:
            print(f"   ✅ Complex relationship query successful:")
            print(f"      📍 Place: {result[0]} (${result[1]})")
            print(f"      👤 Owner: {result[2]}")
            print(f"      🏖️  Amenities: {result[3]}")
            print(f"      ⭐ Rating: {result[4]} ({result[5]} reviews)")
        
        # Commit all changes
        conn.commit()
        
        # Final database info
        print("\n📊 Final Database Status:")
        
        tables = ['users', 'places', 'reviews', 'amenities', 'place_amenity']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"   📋 {table}: {count} rows")
        
        print(f"\n🎉 DATABASE SETUP COMPLETED!")
        print(f"📍 Database file: {db_file}")
        print(f"📊 Database size: {os.path.getsize(db_file)} bytes")
        
        print(f"\n🔑 Admin Login Credentials:")
        print(f"   Email: admin@hbnb.io")
        print(f"   Password: admin1234")
        
        print(f"\n🚀 You can now:")
        print(f"   1. Connect your Flask app to this database")
        print(f"   2. Use: sqlite3 {db_file}")
        print(f"   3. Run SQL queries directly")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during database creation: {e}")
        return False
        
    finally:
        cursor.close()
        conn.close()

def main():
    """Main function."""
    success = create_database()
    if success:
        print("\n✅ SUCCESS: Database ready for use!")
    else:
        print("\n❌ FAILED: Database creation unsuccessful")

if __name__ == "__main__":
    main()
    