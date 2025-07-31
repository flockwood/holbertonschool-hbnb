# Create a test script: test_review_setup.py
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def setup_test_data():
    print("🔧 Setting up test data for review testing...")
    
    # 1. Login as admin
    print("\n1. Logging in as admin...")
    admin_login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@hbnb.com",
        "password": "admin123"
    })
    
    if admin_login.status_code != 200:
        print("❌ Admin login failed!")
        return
    
    admin_token = admin_login.json()['access_token']
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("✅ Admin logged in")
    
    # 2. Create test users
    print("\n2. Creating test users...")
    users = []
    
    test_users = [
        {"first_name": "Alice", "last_name": "Reviewer", "email": "alice@review.com", "password": "test123"},
        {"first_name": "Bob", "last_name": "Tester", "email": "bob@review.com", "password": "test123"}
    ]
    
    for user_data in test_users:
        response = requests.post(f"{BASE_URL}/users/", json=user_data, headers=admin_headers)
        if response.status_code == 201:
            users.append(response.json())
            print(f"✅ Created user: {user_data['email']}")
        elif response.status_code == 409:
            print(f"ℹ️  User already exists: {user_data['email']}")
            # Get existing user
            all_users = requests.get(f"{BASE_URL}/users/").json()
            existing = next((u for u in all_users if u['email'] == user_data['email']), None)
            if existing:
                users.append(existing)
    
    # 3. Create amenities
    print("\n3. Creating amenities...")
    amenities = []
    
    for name in ["WiFi", "Pool", "Parking"]:
        response = requests.post(f"{BASE_URL}/amenities/", 
                               json={"name": name}, 
                               headers=admin_headers)
        if response.status_code == 201:
            amenities.append(response.json())
            print(f"✅ Created amenity: {name}")
        elif response.status_code == 409:
            print(f"ℹ️  Amenity already exists: {name}")
    
    # 4. Create places owned by different users
    print("\n4. Creating test places...")
    
    # Login as Alice to create her place
    alice_login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "alice@review.com",
        "password": "test123"
    })
    
    if alice_login.status_code == 200:
        alice_token = alice_login.json()['access_token']
        alice_headers = {"Authorization": f"Bearer {alice_token}"}
        
        # Alice creates a place
        alice_place = {
            "title": "Alice's Cozy Apartment",
            "description": "A beautiful apartment in the city center",
            "price": 100,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "amenities": [amenities[0]['id']] if amenities else []
        }
        
        response = requests.post(f"{BASE_URL}/places/", json=alice_place, headers=alice_headers)
        if response.status_code == 201:
            place = response.json()
            print(f"✅ Created place: {alice_place['title']} (ID: {place['id']})")
            print(f"   URL: http://127.0.0.1:5000/place.html?id={place['id']}")
    
    # Login as Bob to create his place
    bob_login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "bob@review.com",
        "password": "test123"
    })
    
    if bob_login.status_code == 200:
        bob_token = bob_login.json()['access_token']
        bob_headers = {"Authorization": f"Bearer {bob_token}"}
        
        # Bob creates a place
        bob_place = {
            "title": "Bob's Beach House",
            "description": "Relaxing beach house with ocean view",
            "price": 200,
            "latitude": 25.7617,
            "longitude": -80.1918,
            "amenities": [amenities[1]['id']] if len(amenities) > 1 else []
        }
        
        response = requests.post(f"{BASE_URL}/places/", json=bob_place, headers=bob_headers)
        if response.status_code == 201:
            place = response.json()
            print(f"✅ Created place: {bob_place['title']} (ID: {place['id']})")
            print(f"   URL: http://127.0.0.1:5000/place.html?id={place['id']}")
    
    print("\n✅ Test data setup complete!")
    print("\n📝 Test Instructions:")
    print("1. Login as Bob (bob@review.com / test123)")
    print("2. Go to Alice's place and leave a review")
    print("3. Login as Alice (alice@review.com / test123)")
    print("4. Go to Bob's place and leave a review")
    print("5. Try to review your own place (should fail)")
    print("6. Try to review a place twice (should fail)")

if __name__ == "__main__":
    setup_test_data()