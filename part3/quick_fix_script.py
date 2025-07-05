#!/usr/bin/env python3
"""
Quick Fix Script for Relationship Testing
Resolves common issues and prepares for testing.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def check_server_status():
    """Check if server is running and responsive."""
    print("🔍 Checking server status...")
    try:
        response = requests.get(f"{BASE_URL}/amenities/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responsive")
            return True
        else:
            print(f"⚠️  Server responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running:")
        print("   python run.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ Server timeout. Server might be overloaded.")
        return False

def fix_admin_user():
    """Ensure admin user exists and has proper privileges."""
    print("\n🛡️  Checking admin user...")
    
    # Try to login as admin
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "admin@hbnb.com",
            "password": "admin123"
        })
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Admin user login successful")
            
            # Check admin privileges
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            protected_response = requests.get(f"{BASE_URL}/auth/protected", headers=headers)
            
            if protected_response.status_code == 200:
                user_info = protected_response.json()
                is_admin = user_info.get('is_admin', False)
                print(f"🛡️  Admin privileges: {'✅ Active' if is_admin else '❌ Missing'}")
                
                if not is_admin:
                    print("⚠️  Admin user exists but lacks admin privileges!")
                    print("   This might be a database issue. Try running migration again.")
                
                return token_data['access_token'] if is_admin else None
            else:
                print("❌ Cannot verify admin privileges")
                return None
        else:
            print("❌ Admin login failed")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error checking admin user: {e}")
        return None

def create_test_data(admin_token):
    """Create basic test data if it doesn't exist."""
    if not admin_token:
        print("❌ No admin token, cannot create test data")
        return False
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    print("\n📊 Creating basic test data...")
    
    # 1. Ensure we have some amenities
    print("1. Checking amenities...")
    amenities_response = requests.get(f"{BASE_URL}/amenities/")
    existing_amenities = amenities_response.json() if amenities_response.status_code == 200 else []
    
    basic_amenities = ["WiFi", "Pool", "Gym"]
    created_amenities = []
    
    for amenity_name in basic_amenities:
        # Check if exists
        exists = any(a['name'] == amenity_name for a in existing_amenities)
        
        if not exists:
            response = requests.post(f"{BASE_URL}/amenities/", json={"name": amenity_name}, headers=headers)
            if response.status_code == 201:
                amenity = response.json()
                created_amenities.append(amenity)
                print(f"   ✅ Created amenity: {amenity_name}")
            else:
                print(f"   ❌ Failed to create amenity {amenity_name}: {response.text}")
        else:
            existing_amenity = next(a for a in existing_amenities if a['name'] == amenity_name)
            created_amenities.append(existing_amenity)
            print(f"   ♻️  Found existing amenity: {amenity_name}")
    
    # 2. Ensure we have some test users
    print("\n2. Checking test users...")
    users_response = requests.get(f"{BASE_URL}/users/")
    existing_users = users_response.json() if users_response.status_code == 200 else []
    
    test_users_data = [
        {"first_name": "Alice", "last_name": "Johnson", "email": "alice@test.com", "password": "test123"},
        {"first_name": "Bob", "last_name": "Smith", "email": "bob@test.com", "password": "test123"}
    ]
    
    created_users = []
    
    for user_data in test_users_data:
        # Check if exists
        exists = any(u['email'] == user_data['email'] for u in existing_users)
        
        if not exists:
            response = requests.post(f"{BASE_URL}/users/", json=user_data, headers=headers)
            if response.status_code == 201:
                user = response.json()
                created_users.append(user)
                print(f"   ✅ Created user: {user_data['first_name']} {user_data['last_name']}")
            else:
                print(f"   ❌ Failed to create user {user_data['first_name']}: {response.text}")
        else:
            existing_user = next(u for u in existing_users if u['email'] == user_data['email'])
            created_users.append(existing_user)
            print(f"   ♻️  Found existing user: {user_data['first_name']} {user_data['last_name']}")
    
    print(f"\n📈 Test data summary:")
    print(f"   🏖️  Amenities: {len(created_amenities)} available")
    print(f"   👥 Users: {len(created_users)} available")
    
    return len(created_amenities) >= 2 and len(created_users) >= 2

def test_basic_relationships(admin_token):
    """Test basic relationship functionality."""
    if not admin_token:
        print("❌ No admin token, cannot test relationships")
        return False
    
    print("\n🔗 Testing basic relationships...")
    
    try:
        # Get users
        users_response = requests.get(f"{BASE_URL}/users/")
        users = users_response.json() if users_response.status_code == 200 else []
        test_users = [u for u in users if not u.get('is_admin', False)]
        
        if len(test_users) < 1:
            print("❌ No test users available")
            return False
        
        # Login as test user
        test_user = test_users[0]
        login_response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": test_user['email'],
            "password": "test123"
        })
        
        if login_response.status_code != 200:
            print(f"❌ Cannot login as test user: {login_response.status_code}")
            return False
        
        user_token = login_response.json()['access_token']
        user_headers = {"Authorization": f"Bearer {user_token}"}
        
        # Get amenities
        amenities_response = requests.get(f"{BASE_URL}/amenities/")
        amenities = amenities_response.json() if amenities_response.status_code == 200 else []
        
        if len(amenities) < 1:
            print("❌ No amenities available")
            return False
        
        # Create a test place with amenities (testing relationships)
        place_data = {
            "title": "Test Relationship Place",
            "description": "Testing place-amenity and user-place relationships",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "amenities": [amenities[0]['id']]
        }
        
        place_response = requests.post(f"{BASE_URL}/places/", json=place_data, headers=user_headers)
        
        if place_response.status_code != 201:
            print(f"❌ Failed to create test place: {place_response.status_code}")
            print(f"   Response: {place_response.text}")
            return False
        
        place = place_response.json()
        print(f"✅ Created test place: {place['title']}")
        
        # Test getting place details (should include owner and amenities via relationships)
        detail_response = requests.get(f"{BASE_URL}/places/{place['id']}")
        
        if detail_response.status_code != 200:
            print(f"❌ Failed to get place details: {detail_response.status_code}")
            return False
        
        place_detail = detail_response.json()
        
        # Check relationships
        has_owner = 'owner' in place_detail and place_detail['owner']
        has_amenities = 'amenities' in place_detail and len(place_detail['amenities']) > 0
        
        print(f"✅ Place details retrieved:")
        print(f"   👤 Owner relationship: {'✅ Working' if has_owner else '❌ Missing'}")
        print(f"   🏖️  Amenity relationship: {'✅ Working' if has_amenities else '❌ Missing'}")
        
        if has_owner:
            owner = place_detail['owner']
            print(f"      Owner: {owner['first_name']} {owner['last_name']}")
        
        if has_amenities:
            print(f"      Amenities: {', '.join([a['name'] for a in place_detail['amenities']])}")
        
        return has_owner and has_amenities
        
    except Exception as e:
        print(f"❌ Error testing relationships: {e}")
        return False

def main():
    """Main fix function."""
    print("🔧 QUICK FIX FOR RELATIONSHIP TESTING")
    print("=" * 50)
    
    # Step 1: Check server
    if not check_server_status():
        return
    
    # Step 2: Check/fix admin user
    admin_token = fix_admin_user()
    if not admin_token:
        print("\n❌ Cannot proceed without working admin user")
        print("💡 Try running: python migration_script.py")
        return
    
    # Step 3: Create test data
    if not create_test_data(admin_token):
        print("\n❌ Failed to create test data")
        return
    
    # Step 4: Test basic relationships
    if not test_basic_relationships(admin_token):
        print("\n❌ Basic relationship test failed")
        return
    
    print("\n" + "=" * 50)
    print("✅ QUICK FIX COMPLETED!")
    print("🚀 Your relationships should now work properly.")
    print("\n📝 Next steps:")
    print("   1. Run: python relationship_test_script.py")
    print("   2. Or run: python debug_relationships.py")
    print("=" * 50)

if __name__ == "__main__":
    main()