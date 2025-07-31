# check_reviews.py
import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"

def check_all_reviews():
    # Get all places
    places = requests.get(f"{BASE_URL}/places/").json()
    
    print("📋 REVIEW SUMMARY")
    print("=" * 50)
    
    for place in places:
        detail = requests.get(f"{BASE_URL}/places/{place['id']}").json()
        reviews = requests.get(f"{BASE_URL}/reviews/places/{place['id']}/reviews").json()
        
        print(f"\n📍 {detail['title']}")
        print(f"   Owner: {detail['owner']['first_name']} {detail['owner']['last_name']}")
        print(f"   Reviews: {len(reviews)}")
        
        for review in reviews:
            print(f"   ⭐ {review['rating']}/5 - {review['text']}")

if __name__ == "__main__":
    check_all_reviews()