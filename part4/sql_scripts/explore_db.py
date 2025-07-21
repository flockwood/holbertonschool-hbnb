import sqlite3

def explore_database():
    conn = sqlite3.connect('hbnb_raw_sql.db')
    cursor = conn.cursor()
    
    print("=== HBnB Database Explorer ===")
    print()
    
    # Show tables
    print("TABLES:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(f"  - {table[0]}")
    
    print()
    
    # Show users
    print("USERS:")
    cursor.execute("SELECT first_name, last_name, email, is_admin FROM users;")
    users = cursor.fetchall()
    for user in users:
        status = "Admin" if user[3] else "Regular"
        print(f"  - {user[0]} {user[1]} ({user[2]}) - {status}")
    
    print()
    
    # Show amenities
    print("AMENITIES:")
    cursor.execute("SELECT name FROM amenities;")
    amenities = cursor.fetchall()
    for amenity in amenities:
        print(f"  - {amenity[0]}")
    
    print()
    
    # Show places
    print("PLACES:")
    cursor.execute("SELECT title, price, latitude, longitude FROM places;")
    places = cursor.fetchall()
    for place in places:
        print(f"  - {place[0]} - ${place[1]} at ({place[2]}, {place[3]})")
    
    print()
    
    # Show reviews
    print("REVIEWS:")
    cursor.execute("SELECT text, rating FROM reviews;")
    reviews = cursor.fetchall()
    for review in reviews:
        text_preview = review[0][:50] + "..." if len(review[0]) > 50 else review[0]
        print(f"  - {review[1]}/5: \"{text_preview}\"")
    
    print()
    
    # Test relationships
    print("RELATIONSHIP TEST:")
    cursor.execute("""
        SELECT 
            p.title,
            u.first_name || ' ' || u.last_name as owner,
            COUNT(pa.amenity_id) as amenity_count
        FROM places p
        JOIN users u ON p.owner_id = u.id
        LEFT JOIN place_amenity pa ON p.id = pa.place_id
        GROUP BY p.id, p.title, u.first_name, u.last_name;
    """)
    
    results = cursor.fetchall()
    for result in results:
        print(f"  - Place: {result[0]}")
        print(f"    Owner: {result[1]}")
        print(f"    Amenities: {result[2]} attached")
    
    print()
    
    # Show amenities for places
    print("PLACE-AMENITY RELATIONSHIPS:")
    cursor.execute("""
        SELECT 
            p.title,
            a.name
        FROM places p
        JOIN place_amenity pa ON p.id = pa.place_id
        JOIN amenities a ON pa.amenity_id = a.id;
    """)
    
    relationships = cursor.fetchall()
    for rel in relationships:
        print(f"  - {rel[0]} has {rel[1]}")
    
    conn.close()
    print()
    print("Database exploration complete!")

if __name__ == "__main__":
    explore_database()
