import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.facade import HBnBFacade

def test_places():
    facade = HBnBFacade()
    
    # Step 1: Create a user (owner)
    print("1. Creating user (owner)...")
    try:
        user_data = {
            'first_name': 'John',
            'last_name': 'Owner',
            'email': 'owner@test.com',
            'password': 'password123'
        }
        owner = facade.create_user(user_data)
        print(f"✅ Owner created: {owner.id}")
    except Exception as e:
        print(f"❌ Owner creation failed: {e}")
        return
    
    # Step 2: Create an amenity
    print("\n2. Creating amenity...")
    try:
        amenity_data = {'name': 'WiFi'}
        amenity = facade.create_amenity(amenity_data)
        print(f"✅ Amenity created: {amenity.id}")
    except Exception as e:
        print(f"❌ Amenity creation failed: {e}")
        return
    
    # Step 3: Create a place
    print("\n3. Creating place...")
    try:
        place_data = {
            'title': 'Beach House',
            'description': 'Beautiful house by the beach',
            'price': 150.0,
            'latitude': 18.47,
            'longitude': -66.12,
            'owner_id': owner.id,
            'amenities': [amenity.id]
        }
        place = facade.create_place(place_data)
        print(f"✅ Place created: {place.id}")
    except Exception as e:
        print(f"❌ Place creation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Get place details
    print("\n4. Getting place details...")
    try:
        place_details = facade.get_place(place.id)
        print(f"✅ Place details retrieved")
        print(f"Title: {place_details.get('title')}")
        print(f"Owner: {place_details.get('owner', {}).get('first_name')}")
        print(f"Amenities: {len(place_details.get('amenities', []))}")
    except Exception as e:
        print(f"❌ Get place details failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_places()