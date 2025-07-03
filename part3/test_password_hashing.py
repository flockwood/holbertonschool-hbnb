import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_password_hashing():
    print("=== TESTING PASSWORD HASHING ===")
    
    # Test 1: Create user with password
    print("\n1. Testing user creation with password...")
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.secure@example.com",
        "password": "securepassword123"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 201:
        user_id = response.json()['id']
        print(f"✅ User created: {user_id}")
        
        # Verify password is not in response
        if 'password' not in response.json():
            print("✅ Password not returned in creation response")
        else:
            print("❌ Password was returned in creation response")
        
        # Test 2: Get user by ID
        print(f"\n2. Testing GET user by ID...")
        get_response = requests.get(f"{BASE_URL}/users/{user_id}")
        print(f"Status: {get_response.status_code}")
        print(f"Response: {get_response.json()}")
        
        # Verify password is not in GET response
        if 'password' not in get_response.json():
            print("✅ Password not returned in GET response")
        else:
            print("❌ Password was returned in GET response")
            
    else:
        print("❌ User creation failed")

if __name__ == "__main__":
    test_password_hashing()