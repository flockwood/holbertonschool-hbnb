# test_review_functionality.py
import requests
import time

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_review_functionality():
    print("🧪 TESTING REVIEW FUNCTIONALITY")
    print("=" * 50)
    
    # Get all places first
    places = requests.get(f"{BASE_URL}/places/").json()
    if not places:
        print("❌ No places found. Run test_review_setup.py first!")
        return
    
    # Test 1: Successful review
    print("\n✅ Test 1: Submit review as authenticated user")
    
    # Login as Bob
    bob_login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "bob@review.com",
        "password": "test123"
    })
    
    if bob_login.status_code == 200:
        bob_token = bob_login.json()['access_token']
        headers = {"Authorization": f"Bearer {bob_token}"}
        
        # Find a place NOT owned by Bob
        bob_places = []
        for place in places:
            detail = requests.get(f"{BASE_URL}/places/{place['id']}").json()
            if detail['owner']['email'] != "bob@review.com":
                # Bob can review this place
                review_data = {
                    "text": f"Test review at {time.strftime('%Y-%m-%d %H:%M:%S')}",
                    "rating": 4,
                    "place_id": place['id']
                }
                
                response = requests.post(f"{BASE_URL}/reviews/", 
                                       json=review_data, 
                                       headers=headers)
                
                if response.status_code == 201:
                    print(f"   ✅ Successfully reviewed: {detail['title']}")
                else:
                    error = response.json()
                    print(f"   ❌ Failed: {error.get('message', response.text)}")
                break
    
    # Test 2: Unauthenticated review
    print("\n❌ Test 2: Submit review without authentication")
    review_data = {
        "text": "This should fail",
        "rating": 3,
        "place_id": places[0]['id']
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data)
    if response.status_code == 401:
        print("   ✅ Correctly rejected: Authentication required")
    else:
        print(f"   ❌ Unexpected response: {response.status_code}")
    
    # Test 3: Review own place
    print("\n❌ Test 3: Try to review own place")
    
    # Find Bob's own place
    for place in places:
        detail = requests.get(f"{BASE_URL}/places/{place['id']}").json()
        if detail['owner']['email'] == "bob@review.com":
            review_data = {
                "text": "Reviewing my own place",
                "rating": 5,
                "place_id": place['id']
            }
            
            response = requests.post(f"{BASE_URL}/reviews/", 
                                   json=review_data, 
                                   headers=headers)
            
            if response.status_code == 400:
                print("   ✅ Correctly rejected: Cannot review own place")
            else:
                print(f"   ❌ Unexpected response: {response.status_code}")
            break
    
    print("\n✅ Review functionality tests complete!")

if __name__ == "__main__":
    test_review_functionality()