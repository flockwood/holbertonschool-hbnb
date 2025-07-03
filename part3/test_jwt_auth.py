import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_jwt_authentication():
    print("=== TESTING JWT AUTHENTICATION ===")
    
    # Step 1: Create a user first
    print("\n1. Creating a test user...")
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.jwt@example.com",
        "password": "securepassword123"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"User creation status: {response.status_code}")
    
    if response.status_code != 201:
        print("❌ Failed to create user")
        return
    
    print("✅ User created successfully")
    
    # Step 2: Test login with correct credentials
    print("\n2. Testing login with correct credentials...")
    login_data = {
        "email": "john.jwt@example.com",
        "password": "securepassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login status: {response.status_code}")
    print(f"Login response: {response.json()}")
    
    if response.status_code != 200:
        print("❌ Login failed")
        return
    
    # Extract the JWT token
    token = response.json()['access_token']
    print(f"✅ Login successful! Token received.")
    
    # Step 3: Test login with wrong credentials
    print("\n3. Testing login with wrong credentials...")
    wrong_login = {
        "email": "john.jwt@example.com",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=wrong_login)
    print(f"Wrong login status: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ Wrong credentials correctly rejected")
    else:
        print("❌ Wrong credentials not properly handled")
    
    # Step 4: Test protected endpoint without token
    print("\n4. Testing protected endpoint without token...")
    response = requests.get(f"{BASE_URL}/auth/protected")
    print(f"No token status: {response.status_code}")
    
    if response.status_code == 401:
        print("✅ Protected endpoint correctly requires token")
    else:
        print("❌ Protected endpoint should require token")
    
    # Step 5: Test protected endpoint with valid token
    print("\n5. Testing protected endpoint with valid token...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/protected", headers=headers)
    print(f"With token status: {response.status_code}")
    print(f"Protected response: {response.json()}")
    
    if response.status_code == 200:
        print("✅ Protected endpoint accessible with valid token")
    else:
        print("❌ Protected endpoint should be accessible with valid token")

if __name__ == "__main__":
    test_jwt_authentication()