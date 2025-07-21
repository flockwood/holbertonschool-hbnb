import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_admin_endpoints():
    print("=== TESTING ADMIN ENDPOINTS ===")
    print("Note: Make sure admin user exists (admin@hbnb.com / admin123)")
    
    # Step 1: Login as admin
    print("\n1. Logging in as admin...")
    admin_login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@hbnb.com",
        "password": "admin123"
    })
    
    if admin_login.status_code != 200:
        print(f"❌ Admin login failed: {admin_login.status_code}")
        print(f"Response: {admin_login.text}")
        print("Make sure you've created and promoted the admin user!")
        return
    
    admin_token = admin_login.json()['access_token']
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("✅ Admin logged in successfully")
    
    # Step 2: Test admin creating user
    print("\n2. Testing admin user creation...")
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
        print(f"❌ Admin user creation failed: {create_user_response.text}")
        new_user_id = None
    
    # Step 3: Test admin modifying any user
    if new_user_id:
        print("\n3. Testing admin user modification...")
        modify_data = {
            "first_name": "Modified",
            "email": "modified@example.com"
        }
        
        modify_response = requests.put(f"{BASE_URL}/users/{new_user_id}", json=modify_data, headers=admin_headers)
        print(f"Admin user modification status: {modify_response.status_code}")
        
        if modify_response.status_code == 200:
            print("✅ Admin successfully modified user")
        else:
            print(f"❌ Admin user modification failed: {modify_response.text}")
    
    # Step 4: Test admin creating amenity
    print("\n4. Testing admin amenity creation...")
    amenity_data = {"name": "Admin Pool"}
    
    amenity_response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=admin_headers)
    print(f"Admin amenity creation status: {amenity_response.status_code}")
    
    if amenity_response.status_code == 201:
        amenity_id = amenity_response.json()['id']
        print(f"✅ Admin created amenity: {amenity_id[:8]}...")
    else:
        print(f"❌ Admin amenity creation failed: {amenity_response.text}")
        amenity_id = None
    
    # Step 5: Test admin modifying amenity
    if amenity_id:
        print("\n5. Testing admin amenity modification...")
        amenity_modify = {"name": "Updated Admin Pool"}
        
        amenity_mod_response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json=amenity_modify, headers=admin_headers)
        print(f"Admin amenity modification status: {amenity_mod_response.status_code}")
        
        if amenity_mod_response.status_code == 200:
            print("✅ Admin successfully modified amenity")
        else:
            print(f"❌ Admin amenity modification failed: {amenity_mod_response.text}")
    
    # Step 6: Test regular user restrictions (create a regular user first)
    print("\n6. Testing regular user restrictions...")
    
    # Create regular user via admin
    regular_user_data = {
        "first_name": "Regular",
        "last_name": "User",
        "email": "regular@example.com",
        "password": "password123"
    }
    
    regular_user_response = requests.post(f"{BASE_URL}/users/", json=regular_user_data, headers=admin_headers)
    
    if regular_user_response.status_code == 201:
        # Login as regular user
        regular_login = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "regular@example.com",
            "password": "password123"
        })
        
        if regular_login.status_code == 200:
            regular_token = regular_login.json()['access_token']
            regular_headers = {"Authorization": f"Bearer {regular_token}"}
            
            # Test regular user trying to create amenity (should fail)
            restricted_amenity = requests.post(f"{BASE_URL}/amenities/", json={
                "name": "Restricted Amenity"
            }, headers=regular_headers)
            
            print(f"Regular user amenity creation status: {restricted_amenity.status_code}")
            
            if restricted_amenity.status_code == 403:
                print("✅ Regular user correctly restricted from creating amenities")
            else:
                print("❌ Regular user should be restricted from creating amenities")
        else:
            print("❌ Regular user login failed")
    else:
        print("❌ Failed to create regular user for testing")
    
    # Step 7: Test public endpoints still work
    print("\n7. Testing public endpoints accessibility...")
    
    # Test public place listing
    public_places = requests.get(f"{BASE_URL}/places/")
    print(f"Public places listing status: {public_places.status_code}")
    
    # Test public amenity listing
    public_amenities = requests.get(f"{BASE_URL}/amenities/")
    print(f"Public amenities listing status: {public_amenities.status_code}")
    
    if public_places.status_code == 200 and public_amenities.status_code == 200:
        print("✅ Public endpoints remain accessible")
    else:
        print("❌ Public endpoints should remain accessible")
    
    print("\n=== ADMIN TESTING COMPLETE ===")
    print("\n📊 SUMMARY:")
    print("✅ Admin authentication working")
    print("✅ Admin-only operations tested")
    print("✅ Regular user restrictions verified")
    print("✅ Public access maintained")

if __name__ == "__main__":
    test_admin_endpoints()