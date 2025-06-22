import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_user_validation():
    print("=== TESTING USER VALIDATION ===")
    
    # Test 1: Empty fields
    print("\n1. Testing empty user fields...")
    invalid_user = {
        "first_name": "",
        "last_name": "",
        "email": "invalid-email",
        "password": ""
    }
    response = requests.post(f"{BASE_URL}/users/", json=invalid_user)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test 2: Invalid email format
    print("\n2. Testing invalid email format...")
    invalid_email = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "not-an-email",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/users/", json=invalid_email)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

def test_place_validation():
    print("\n=== TESTING PLACE VALIDATION ===")
    
    # Test 1: Invalid coordinates and price
    print("\n1. Testing invalid place data...")
    invalid_place = {
        "title": "",  # Empty title
        "description": "Test",
        "price": -50.0,  # Negative price
        "latitude": 200,  # Invalid latitude (>90)
        "longitude": 300,  # Invalid longitude (>180)
        "owner_id": "fake-owner-id"  # Non-existent owner
    }
    response = requests.post(f"{BASE_URL}/places/", json=invalid_place)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

def test_review_validation():
    print("\n=== TESTING REVIEW VALIDATION ===")
    
    # Test 1: Invalid rating and empty text
    print("\n1. Testing invalid review data...")
    invalid_review = {
        "text": "",  # Empty text
        "rating": 10,  # Invalid rating (>5)
        "user_id": "fake-user-id",  # Non-existent user
        "place_id": "fake-place-id"  # Non-existent place
    }
    response = requests.post(f"{BASE_URL}/reviews/", json=invalid_review)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

def test_get_nonexistent():
    print("\n=== TESTING NON-EXISTENT RESOURCES ===")
    
    # Test getting non-existent user
    print("\n1. Testing non-existent user...")
    response = requests.get(f"{BASE_URL}/users/fake-id")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test getting non-existent place
    print("\n2. Testing non-existent place...")
    response = requests.get(f"{BASE_URL}/places/fake-id")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test getting non-existent review
    print("\n3. Testing non-existent review...")
    response = requests.get(f"{BASE_URL}/reviews/fake-id")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    print("Testing validation and error handling...")
    
    test_user_validation()
    test_place_validation() 
    test_review_validation()
    test_get_nonexistent()
    
    print("\n=== VALIDATION TESTING COMPLETE ===")
