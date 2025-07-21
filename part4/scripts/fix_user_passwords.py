#!/usr/bin/env python3
"""
Fix User Passwords Script
Updates existing test user passwords to known values.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def fix_user_passwords():
    """Fix passwords for existing test users."""
    print("🔑 FIXING USER PASSWORDS")
    print("=" * 40)
    
    # Login as admin
    print("1. Logging in as admin...")
    admin_login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@hbnb.com",
        "password": "admin123"
    })
    
    if admin_login.status_code != 200:
        print("❌ Admin login failed")
        return False
    
    admin_token = admin_login.json()['access_token']
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("✅ Admin authenticated")
    
    # Get all users
    print("\n2. Getting existing users...")
    users_response = requests.get(f"{BASE_URL}/users/")
    if users_response.status_code != 200:
        print("❌ Failed to get users")
        return False
    
    all_users = users_response.json()
    test_users = [u for u in all_users if u['email'] in ['alice@test.com', 'bob@test.com', 'carol@test.com']]
    
    print(f"   Found {len(test_users)} test users")
    
    # Update passwords for test users
    print("\n3. Updating test user passwords...")
    
    for user in test_users:
        print(f"\n   Updating {user['first_name']} {user['last_name']}...")
        
        # Update user with new password
        update_data = {
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "email": user['email'],
            "password": "test123"  # Set known password
        }
        
        response = requests.put(f"{BASE_URL}/users/{user['id']}", 
                              json=update_data, 
                              headers=admin_headers)
        
        if response.status_code == 200:
            print(f"   ✅ Password updated for {user['first_name']}")
            
            # Test login with new password
            login_test = requests.post(f"{BASE_URL}/auth/login", json={
                "email": user['email'],
                "password": "test123"
            })
            
            if login_test.status_code == 200:
                print(f"   ✅ Login test successful for {user['email']}")
            else:
                print(f"   ❌ Login test failed for {user['email']}: {login_test.status_code}")
        else:
            print(f"   ❌ Failed to update password: {response.status_code}")
            print(f"      Response: {response.text}")
    
    return True

def create_fresh_test_users():
    """Create fresh test users with known passwords."""
    print("\n🆕 CREATING FRESH TEST USERS")
    print("=" * 40)
    
    # Login as admin
    admin_login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@hbnb.com",
        "password": "admin123"
    })
    
    if admin_login.status_code != 200:
        print("❌ Admin login failed")
        return False
    
    admin_token = admin_login.json()['access_token']
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Create fresh test users with unique emails
    fresh_users = [
        {"first_name": "TestUser1", "last_name": "Demo", "email": "testuser1@demo.com", "password": "demo123"},
        {"first_name": "TestUser2", "last_name": "Demo", "email": "testuser2@demo.com", "password": "demo123"},
        {"first_name": "TestUser3", "last_name": "Demo", "email": "testuser3@demo.com", "password": "demo123"}
    ]
    
    created_users = []
    
    for user_data in fresh_users:
        print(f"\nCreating {user_data['first_name']}...")
        
        response = requests.post(f"{BASE_URL}/users/", json=user_data, headers=admin_headers)
        
        if response.status_code == 201:
            user = response.json()
            created_users.append(user)
            print(f"   ✅ Created: {user['email']}")
            
            # Test login immediately
            login_test = requests.post(f"{BASE_URL}/auth/login", json={
                "email": user_data['email'],
                "password": user_data['password']
            })
            
            if login_test.status_code == 200:
                print(f"   ✅ Login verified for {user['email']}")
            else:
                print(f"   ❌ Login failed for {user['email']}: {login_test.status_code}")
                
        elif response.status_code == 409:
            print(f"   ♻️  User already exists: {user_data['email']}")
        else:
            print(f"   ❌ Failed to create user: {response.status_code}")
            print(f"      Response: {response.text}")
    
    return len(created_users) > 0

def test_user_login():
    """Test login for various users."""
    print("\n🧪 TESTING USER LOGINS")
    print("=" * 40)
    
    # Test different email/password combinations
    test_combinations = [
        ("alice@test.com", "test123"),
        ("bob@test.com", "test123"),
        ("alice@test.com", "password123"),
        ("bob@test.com", "password123"),
        ("testuser1@demo.com", "demo123"),
        ("testuser2@demo.com", "demo123")
    ]
    
    working_users = []
    
    for email, password in test_combinations:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            print(f"✅ {email} with password '{password}' - SUCCESS")
            working_users.append({"email": email, "password": password})
        else:
            print(f"❌ {email} with password '{password}' - FAILED ({response.status_code})")
    
    print(f"\n📊 Working logins found: {len(working_users)}")
    return working_users

def main():
    """Main function."""
    print("🔑 USER PASSWORD FIX TOOL")
    print("=" * 50)
    
    # Option 1: Try to fix existing users
    print("Attempting to fix existing test user passwords...")
    fix_success = fix_user_passwords()
    
    # Option 2: Create fresh users if fixing didn't work
    if not fix_success:
        print("\nFix attempt failed, creating fresh test users...")
        create_fresh_test_users()
    
    # Test all possible login combinations
    working_users = test_user_login()
    
    if working_users:
        print("\n" + "=" * 50)
        print("✅ USER PASSWORDS FIXED!")
        print("\n🎯 Working test accounts:")
        for user in working_users:
            print(f"   Email: {user['email']}")
            print(f"   Password: {user['password']}")
        
        print("\n🚀 Now you can run:")
        print("   python relationship_test_script.py")
        print("=" * 50)
    else:
        print("\n❌ Could not establish working test users")
        print("Try creating users manually or check API permissions")

if __name__ == "__main__":
    main()