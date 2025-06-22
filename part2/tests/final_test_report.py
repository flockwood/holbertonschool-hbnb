import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def run_final_tests():
    print("=== FINAL API TESTING REPORT ===\n")
    
    results = {
        "passed": 0,
        "failed": 0,
        "tests": []
    }
    
    def log_test(name, expected_status, actual_status, passed):
        results["tests"].append({
            "test": name,
            "expected": expected_status,
            "actual": actual_status,
            "passed": passed
        })
        if passed:
            results["passed"] += 1
            print(f"✅ {name}")
        else:
            results["failed"] += 1
            print(f"❌ {name}")
    
    # Test 1: Valid user creation
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@test.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    log_test("Valid user creation", 201, response.status_code, response.status_code == 201)
    user_id = response.json().get('id') if response.status_code == 201 else None
    
    # Test 2: Invalid user creation
    invalid_user = {"first_name": "", "email": "invalid", "password": ""}
    response = requests.post(f"{BASE_URL}/users/", json=invalid_user)
    log_test("Invalid user creation", 400, response.status_code, response.status_code == 400)
    
    # Test 3: Valid place creation
    if user_id:
        place_data = {
            "title": "Test Place",
            "description": "A test place",
            "price": 100.0,
            "latitude": 18.47,
            "longitude": -66.12,
            "owner_id": user_id
        }
        response = requests.post(f"{BASE_URL}/places/", json=place_data)
        log_test("Valid place creation", 201, response.status_code, response.status_code == 201)
        place_id = response.json().get('id') if response.status_code == 201 else None
        
        # Test 4: Valid review creation
        if place_id:
            review_data = {
                "text": "Great place!",
                "rating": 5,
                "user_id": user_id,
                "place_id": place_id
            }
            response = requests.post(f"{BASE_URL}/reviews/", json=review_data)
            log_test("Valid review creation", 201, response.status_code, response.status_code == 201)
            review_id = response.json().get('id') if response.status_code == 201 else None
            
            # Test 5: Get review by ID
            if review_id:
                response = requests.get(f"{BASE_URL}/reviews/{review_id}")
                log_test("Get review by ID", 200, response.status_code, response.status_code == 200)
                
                # Test 6: Update review
                update_data = {
                    "text": "Updated review!",
                    "rating": 4,
                    "user_id": user_id,
                    "place_id": place_id
                }
                response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=update_data)
                log_test("Update review", 200, response.status_code, response.status_code == 200)
                
                # Test 7: Delete review
                response = requests.delete(f"{BASE_URL}/reviews/{review_id}")
                log_test("Delete review", 200, response.status_code, response.status_code == 200)
    
    # Test 8: Get all entities
    response = requests.get(f"{BASE_URL}/users/")
    log_test("Get all users", 200, response.status_code, response.status_code == 200)
    
    response = requests.get(f"{BASE_URL}/places/")
    log_test("Get all places", 200, response.status_code, response.status_code == 200)
    
    response = requests.get(f"{BASE_URL}/reviews/")
    log_test("Get all reviews", 200, response.status_code, response.status_code == 200)
    
    # Test 9: 404 errors
    response = requests.get(f"{BASE_URL}/users/fake-id")
    log_test("404 for non-existent user", 404, response.status_code, response.status_code == 404)
    
    # Print final summary
    print(f"\n=== FINAL RESULTS ===")
    print(f"✅ Tests Passed: {results['passed']}")
    print(f"❌ Tests Failed: {results['failed']}")
    print(f"📊 Success Rate: {(results['passed']/(results['passed']+results['failed'])*100):.1f}%")
    
    if results['failed'] == 0:
        print("\n🎉 ALL TESTS PASSED! Your API is working perfectly!")
    else:
        print(f"\n⚠️ {results['failed']} tests failed. Review the issues above.")

if __name__ == "__main__":
    run_final_tests()