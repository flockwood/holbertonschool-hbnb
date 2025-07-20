import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_admin_endpoints():
    print("=== TESTING ADMIN ENDPOINTS ===")
    
    # Step 1: Create admin user
    print("\n1. Creating admin user...")
    exec(open('create_admin.py').read())
    
    # Step 2: Login as admin
    print("\n2. Logging in as admin...")
    admin_login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@hbnb.com",
        "password": "admin123"
    })
    
    if admin_login.status_code != 200:
        print("❌ Admin login failed")
        return
    
    admin_token = admin_login.json()['access_token']
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("✅ Admin logged in successfully")
    
    # Step 3: Test admin creating user
    print("\n3. Testing admin user creation...")
    new_user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "password123"
    }
    
    create_user_response = requests.post(f"{BASE_URL}/users/", json=new_user_data, headers=admin_headers)
    print(f"Admin user creation status: {create_user_response.status_code}")
    
    if create_user_response.status_code == 201:
        new_user_id = create_user_response.json()['id']
        print(f"✅ Admin created user: {new_user_id[:8]}...")
    else:
        print("❌ Admin user creation failed")
        return
    
    # Step 4: Test admin modifying any user
    print("\n4. Testing admin user modification...")
    modify_data = {
        "first_name": "Modified",
        "email": "modified@example.com"
    }
    
    modify_response = requests.put(f"{BASE_URL}/users/{new_user_id}", json=modify_data, headers=admin_headers)
    print(f"Admin user modification status: {modify_response.status_code}")
    
    if modify_response.status_code == 200:
        print("✅ Admin successfully modified user")
    else:
        print("❌ Admin user modification failed")
    
    # Step 5: Test admin creating amenity
    print("\n5. Testing admin amenity creation...")
    amenity_data = {"name": "Admin Pool"}
    
    amenity_response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=admin_headers)
    print(f"Admin amenity creation status: {amenity_response.status_code}")
    
    if amenity_response.status_code == 201:
        amenity_id = amenity_response.json()['id']
        print(f"✅ Admin created amenity: {amenity_id[:8]}...")
    else:
        print("❌ Admin amenity creation failed")
        return
    
    # Step 6: Test admin modifying amenity
    print("\n6. Testing admin amenity modification...")
    amenity_modify = {"name": "Updated Admin Pool"}
    
    amenity_mod_response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json=amenity_modify, headers=admin_headers)
    print(f"Admin amenity modification status: {amenity_mod_response.status_code}")
    
    if amenity_mod_response.status_code == 200:
        print("✅ Admin successfully modified amenity")
    else:
        print("❌ Admin amenity modification failed")
    
    # Step 7: Test non-admin access restrictions
    print("\n7. Testing non-admin restrictions...")
    
    # Create regular user
    regular_user = {
        "first_name": "Regular",
        "last_name": "User",
        "email": "regular@example.com",
        "password": "password123"
    }
    
    # Use public endpoint for user creation (since we made it admin-only)
    # First create via facade or temporarily allow public creation
    print("Creating regular user via admin...")
    regular_response = requests.post(f"{BASE_URL}/users/", json=regular_user, headers=admin_headers)
    
    if regular_response.status_code == 201:
        # Login as regular user
        regular_login = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "regular@example.com",
            "password": "password123"
        })
        
        if regular_login.status_code == 200:
            regular_token = regular_login.json()['access_token']
            regular_headers = {"Authorization": f"Bearer {regular_token}"}
            
            # Test regular user trying to create amenity
            restricted_amenity = requests.post(f"{BASE_URL}/amenities/", json={"name": "Restricted"}, headers=regular_headers)
            print(f"Regular user amenity creation status: {restricted_amenity.status_code}")
            
            if restricted_amenity.status_code == 403:
                print("✅ Regular user correctly restricted from creating amenities")
            else:
                print("❌ Regular user should be restricted from creating amenities")

if __name__ == "__main__":
    test_admin_endpoints()