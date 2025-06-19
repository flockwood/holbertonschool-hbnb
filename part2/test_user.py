import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.user import User
from app.services.facade import HBnBFacade

# Test 1: Direct User creation (we know this works)
try:
    print("1. Testing direct user creation...")
    user = User("John", "Doe", "john@test.com", "password123")
    print("✅ Direct user creation successful!")
except Exception as e:
    print(f"❌ Direct user creation failed: {e}")

# Test 2: Facade user creation
try:
    print("\n2. Testing facade user creation...")
    facade = HBnBFacade()
    user_data = {
        'first_name': 'Jane',
        'last_name': 'Smith', 
        'email': 'jane@test.com',
        'password': 'password123'
    }
    new_user = facade.create_user(user_data)
    print("✅ Facade user creation successful!")
    print(f"User ID: {new_user.id}")
except Exception as e:
    print(f"❌ Facade user creation failed: {e}")
    import traceback
    traceback.print_exc()