import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.facade import HBnBFacade

def test_reviews():
    facade = HBnBFacade()
    
    # Step 1: Create a user
    print("1. Creating user...")
    try:
        user_data = {
            'first_name': 'John',
            'last_name': 'Reviewer',
            'email': 'reviewer@test.com',
            'password': 'password123'
        }
        user = facade.create_user(user_data)
        print(f"✅ User created: {user.id}")
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        return
    
    # Step 2: Create a place
    print("\n2. Creating place...")
    try:
        place_data = {
            'title': 'Test Place',
            'description': 'A test place',
            'price': 100.0,
            'latitude': 18.47,
            'longitude': -66.12,
            'owner_id': user.id
        }
        place = facade.create_place(place_data)
        print(f"✅ Place created: {place.id}")
    except Exception as e:
        print(f"❌ Place creation failed: {e}")
        return
    
    # Step 3: Create a review
    print("\n3. Creating review...")
    try:
        review_data = {
            'text': 'Great place to stay!',
            'rating': 5,
            'user_id': user.id,
            'place_id': place.id
        }
        review = facade.create_review(review_data)
        print(f"✅ Review created: {review.id}")
        print(f"Rating: {review.rating}")
    except Exception as e:
        print(f"❌ Review creation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Get reviews by place
    print("\n4. Getting reviews for place...")
    try:
        reviews = facade.get_reviews_by_place(place.id)
        print(f"✅ Found {len(reviews)} reviews for place")
    except Exception as e:
        print(f"❌ Get reviews failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_reviews()