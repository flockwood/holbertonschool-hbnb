import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_place_validation_with_valid_owner():
    print("=== TESTING PLACE VALIDATION WITH VALID OWNER ===")
    
    # First, create a valid user
    print("1. Creating a valid user...")
    user_data = {
        "first_name": "Test",
        "last_name": "Owner",
        "email": "owner@test.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    if response.status_code == 201:
        user_id = response.json()['id']
        print(f"✅ User created: {user_id}")
    else:
        print("❌ Failed to create user")
        return
    
    # Now test place with invalid data but valid owner
    print("\n2. Testing place with invalid coordinates but valid owner...")
    invalid_place = {
        "title": "",  # Empty title
        "description": "Test place",
        "price": -100.0,  # Negative price
        "latitude": 200,  # Invalid latitude
        "longitude": 300,  # Invalid longitude
        "owner_id": user_id  # Valid owner
    }
    response = requests.post(f"{BASE_URL}/places/", json=invalid_place)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_place_validation_with_valid_owner()