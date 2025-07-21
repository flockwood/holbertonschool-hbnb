#!/usr/bin/env python3
"""
Debug Relationships Script
Helps diagnose and fix relationship issues.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def debug_admin_access():
    """Test admin access and capabilities."""
    print("🔧 DEBUGGING ADMIN ACCESS")
    print("=" * 40)
    
    # Test admin login
    print("1. Testing admin login...")
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@hbnb.com",
            "password": "admin123"
        })
        
        if response.status_code == 200:
            token = response.json()['access_token']
            print("   ✅ Admin login successful")
            
            # Test protected endpoint
            print("2. Testing admin protected access...")
            headers = {"Authorization": f"Bearer {token}"}
            protected_response = requests.get(f"{BASE_URL}/auth/protected", headers=headers)
            
            if protected_response.status_code == 200:
                data = protected_response.json()
                print(f"   ✅ Protected access successful")
                print(f"   👤 User ID: {data.get('user_id', 'N/A')}")
                print(f"   🛡️  Is Admin: {data.get('is_admin', False)}")
            else:
                print(f"   ❌ Protected access failed: {protected_response.status_code}")
                
            return token
        else:
            print(f"   ❌ Admin login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server. Is it running on port 5000?")
        return None

def debug_amenities(admin_token):
    """Debug amenity creation issues."""
    print("\n🏖️  DEBUGGING AMENITIES")
    print("=" * 40)
    
    if not admin_token:
        print("❌ No admin token available")
        return []
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Get existing amenities
    print("1. Checking existing amenities...")
    try:
        response = requests.get(f"{BASE_URL}/amenities/")
        if response.status_code == 200:
            existing = response.json()
            print(f"   📊 Found {len(existing)} existing amenities:")
            for amenity in existing:
                print(f"      - {amenity['name']} ({amenity['id'][:8]}...)")
        else:
            print(f"   ❌ Failed to get amenities: {response.status_code}")
            existing = []
    except Exception as e:
        print(f"   ❌ Error getting amenities: {e}")
        existing = []
    
    # Try to create one new amenity
    print("\n2. Testing amenity creation...")
    test_amenity_name = "Test-Debug-Amenity"
    
    # Check if it already exists
    existing_names = [a['name'] for a in existing]
    if test_amenity_name in existing_names:
        print(f"   ⚠️  {test_amenity_name} already exists")
        return existing
    
    try:
        response = requests.post(f"{BASE_URL}/amenities/", json={
            "name": test_amenity_name
        }, headers=headers)
        
        if response.status_code == 201:
            new_amenity = response.json()
            print(f"   ✅ Created test amenity: {new_amenity['name']}")
            existing.append(new_amenity)
        elif response.status_code == 403:
            print("   ❌ Access denied - admin privileges required")
        elif response.status_code == 409:
            print("   ⚠️  Amenity already exists")
        else:
            print(f"   ❌ Failed to create amenity: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error creating amenity: {e}")
    
    return existing

def debug_users(admin_token):
    """Debug user creation and authentication."""
    print("\n👥 DEBUGGING USERS")
    print("=" * 40)
    
    if not admin_token:
        print("❌ No admin token available")
        return []
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Get existing users
    print("1. Checking existing users...")
    try:
        response = requests.get(f"{BASE_URL}/users/")
        if response.status_code == 200:
            users = response.json()
            print(f"   📊 Found {len(users)} existing users:")
            for user in users[:5]:  # Show first 5
                print(f"      - {user['first_name']} {user['last_name']} ({user['email']})")
        else:
            print(f"   ❌ Failed to get users: {response.status_code}")
            users = []
    except Exception as e:
        print(f"   ❌ Error getting users: {e}")
        users = []
    
    # Try to create a test user
    print("\n2. Testing user creation...")
    test_user = {
        "first_name": "Debug",
        "last_name": "User",
        "email": "debug@test.com",
        "password": "debug123"
    }
    
    # Check if user already exists
    existing_emails = [u['email'] for u in users]
    if test_user['email'] in existing_emails:
        print(f"   ⚠️  User {test_user['email']} already exists")
        return users
    
    try:
        response = requests.post(f"{BASE_URL}/users/", json=test_user, headers=headers)
        
        if response.status_code == 201:
            new_user = response.json()
            print(f"   ✅ Created test user: {new_user['email']}")
            users.append(new_user)
            
            # Test login for new user
            print("3. Testing new user login...")
            login_response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": test_user['email'],
                "password": test_user['password']
            })
            
            if login_response.status_code == 200:
                print("   ✅ New user login successful")
            else:
                print(f"   ❌ New user login failed: {login_response.status_code}")
                
        else:
            print(f"   ❌ Failed to create user: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error creating user: {e}")
    
    return users

def debug_places(admin_token, users, amenities):
    """Debug place creation with relationships."""
    print("\n🏠 DEBUGGING PLACES")
    print("=" * 40)
    
    if not admin_token:
        print("❌ No admin token available")
        return []
    
    if not users:
        print("❌ No users available for testing")
        return []
    
    # Use first non-admin user
    test_user = next((u for u in users if not u.get('is_admin', False)), users[0])
    
    # Login as test user
    print("1. Logging in as test user...")
    try:
        login_response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": test_user['email'],
            "password": "password123"  # Default password from tests
        })
        
        if login_response.status_code != 200:
            # Try alternative passwords
            for password in ["debug123", "admin123"]:
                login_response = requests.post(f"{BASE_URL}/auth/login", json={
                    "email": test_user['email'],
                    "password": password
                })
                if login_response.status_code == 200:
                    break
        
        if login_response.status_code == 200:
            user_token = login_response.json()['access_token']
            user_headers = {"Authorization": f"Bearer {user_token}"}
            print(f"   ✅ Logged in as {test_user['first_name']} {test_user['last_name']}")
        else:
            print(f"   ❌ Failed to login as test user: {login_response.status_code}")
            return []
            
    except Exception as e:
        print(f"   ❌ Error logging in: {e}")
        return []
    
    # Try to create a place
    print("2. Testing place creation...")
    place_data = {
        "title": "Debug Test Place",
        "description": "A place for testing relationships",
        "price": 99.99,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "amenities": [amenities[0]['id']] if amenities else []
    }
    
    try:
        response = requests.post(f"{BASE_URL}/places/", json=place_data, headers=user_headers)
        
        if response.status_code == 201:
            new_place = response.json()
            print(f"   ✅ Created test place: {new_place['title']}")
            
            # Test getting place details
            print("3. Testing place details with relationships...")
            detail_response = requests.get(f"{BASE_URL}/places/{new_place['id']}")
            
            if detail_response.status_code == 200:
                place_detail = detail_response.json()
                print("   ✅ Place details retrieved:")
                print(f"      📍 Title: {place_detail['title']}")
                
                if 'owner' in place_detail:
                    owner = place_detail['owner']
                    print(f"      👤 Owner: {owner['first_name']} {owner['last_name']}")
                else:
                    print("      ⚠️  No owner information in response")
                
                amenities_list = place_detail.get('amenities', [])
                print(f"      🏖️  Amenities: {len(amenities_list)} found")
                for amenity in amenities_list:
                    print(f"         - {amenity['name']}")
                    
            else:
                print(f"   ❌ Failed to get place details: {detail_response.status_code}")
                
            return [new_place]
            
        else:
            print(f"   ❌ Failed to create place: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error creating place: {e}")
    
    return []

def main():
    """Main debug function."""
    print("🔍 RELATIONSHIP DEBUGGING TOOL")
    print("=" * 50)
    print("This tool will help diagnose relationship issues step by step.")
    print()
    
    # Step 1: Test admin access
    admin_token = debug_admin_access()
    
    # Step 2: Test amenities
    amenities = debug_amenities(admin_token)
    
    # Step 3: Test users
    users = debug_users(admin_token)
    
    # Step 4: Test places
    places = debug_places(admin_token, users, amenities)
    
    # Summary
    print("\n📊 DEBUG SUMMARY")
    print("=" * 50)
    print(f"✅ Admin access: {'Working' if admin_token else 'Failed'}")
    print(f"📊 Amenities available: {len(amenities)}")
    print(f"👥 Users available: {len(users)}")
    print(f"🏠 Places created: {len(places)}")
    
    if admin_token and amenities and users:
        print("\n🎉 Basic relationships appear to be working!")
        print("Try running the full test again: python relationship_test_script.py")
    else:
        print("\n⚠️  Some issues detected. Check the output above for details.")

if __name__ == "__main__":
    main()