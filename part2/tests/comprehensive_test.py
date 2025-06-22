import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_user_endpoints():
    print("=== TESTING USER ENDPOINTS ===")
    
    # Test 1: Valid user creation
    print("\n1. Testing valid user creation...")
    user_data = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        user_id = response.json()['id']
        print(f"✅ User created successfully: {user_id}")
        return user_id
    else:
        print(f"❌ Failed: {response.text}")
        return None
    
    # Test 2: Invalid user creation (empty fields)
    print("\n2. Testing invalid user creation (empty fields)...")
    invalid_user = {
        "first_name": "",
        "last_name": "",
        "email": "invalid-email",
        "password": ""
    }
    response = requests.post(f"{BASE_URL}/users/", json=invalid_user)
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print("✅ Validation working correctly")
    else:
        print(f"❌ Expected 400, got {response.status_code}")

def test_place_endpoints(user_id):
    print("\n=== TESTING PLACE ENDPOINTS ===")
    
    # Test 1: Valid place creation
    print("\n1. Testing valid place creation...")
    place_data = {
        "title": "Beach House",
        "description": "Beautiful beach house",
        "price": 150.0,
        "latitude": 18.47,
        "longitude": -66.12,
        "owner_id": user_id
    }
    response = requests.post(f"{BASE_URL}/places/", json=place_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        place_id = response.json()['id']
        print(f"✅ Place created successfully: {place_id}")
        return place_id
    else:
        print(f"❌ Failed: {response.text}")
        return None
    
    # Test 2: Invalid place (bad coordinates)
    print("\n2. Testing invalid place (bad coordinates)...")
    invalid_place = {
        "title": "Bad Place",
        "description": "Invalid coordinates",
        "price": -50.0,  # Negative price
        "latitude": 200,  # Invalid latitude
        "longitude": 300,  # Invalid longitude
        "owner_id": user_id
    }
    response = requests.post(f"{BASE_URL}/places/", json=invalid_place)
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print("✅ Validation working correctly")
    else:
        print(f"❌ Expected 400, got {response.status_code}")

def test_review_endpoints(user_id, place_id):
    print("\n=== TESTING REVIEW ENDPOINTS ===")
    
    # Test 1: Valid review creation
    print("\n1. Testing valid review creation...")
    review_data = {
        "text": "Amazing place!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        review_id = response.json()['id']
        print(f"✅ Review created successfully: {review_id}")
        return review_id
    else:
        print(f"❌ Failed: {response.text}")
        return None
    
    # Test 2: Invalid review (bad rating)
    print("\n2. Testing invalid review (bad rating)...")
    invalid_review = {
        "text": "",  # Empty text
        "rating": 10,  # Invalid rating (should be 1-5)
        "user_id": user_id,
        "place_id": place_id
    }
    response = requests.post(f"{BASE_URL}/reviews/", json=invalid_review)
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print("✅ Validation working correctly")
    else:
        print(f"❌ Expected 400, got {response.status_code}")

if __name__ == "__main__":
    print("Starting comprehensive API testing...")
    
    # Run tests in sequence
    user_id = test_user_endpoints()
    if user_id:
        place_id = test_place_endpoints(user_id)
        if place_id:
            review_id = test_review_endpoints(user_id, place_id)
    
    print("\n=== TESTING COMPLETE ===")
