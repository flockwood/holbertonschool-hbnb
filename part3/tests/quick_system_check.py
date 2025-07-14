import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
Quick System Health Check
Fast verification that everything is working.
"""

import requests
import sqlite3
import os

def quick_check():
    print("🚀 QUICK HBNB SYSTEM CHECK")
    print("=" * 30)
    
    # 1. Check Flask server
    print("\n1. Flask Server:")
    try:
        response = requests.get("http://127.0.0.1:5000/api/v1/amenities/", timeout=3)
        if response.status_code == 200:
            print("   ✅ Server running")
        else:
            print(f"   ⚠️  Server responding but status: {response.status_code}")
    except:
        print("   ❌ Server not running - Start with: python run.py")
    
    # 2. Check databases
    print("\n2. Databases:")
    
    # SQLAlchemy database
    sqlalchemy_db_path = "./instance/development.db"
    if os.path.exists(sqlalchemy_db_path):
        print("   ✅ SQLAlchemy database exists")
        try:
            conn = sqlite3.connect(sqlalchemy_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"      📊 {user_count} users in SQLAlchemy DB")
            conn.close()
        except:
            print("   ⚠️  SQLAlchemy database has issues")
    else:
        print("   ❌ SQLAlchemy database missing")
        print(f"      Looking for: {sqlalchemy_db_path}")
        # Check if it's in current directory instead
        if os.path.exists("development.db"):
            print("      Found in current directory: development.db")
    
    # Raw SQL database
    if os.path.exists("sql_scripts/hbnb_raw_sql.db"):
        print("   ✅ Raw SQL database exists")
        try:
            conn = sqlite3.connect("sql_scripts/hbnb_raw_sql.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            print(f"      📊 {user_count} users in Raw SQL DB")
            conn.close()
        except:
            print("   ⚠️  Raw SQL database has issues")
    else:
        print("   ❌ Raw SQL database missing")
    
    # 3. Check authentication
    print("\n3. Authentication:")
    try:
        response = requests.post("http://127.0.0.1:5000/api/v1/auth/login", 
                               json={"email": "admin@hbnb.com", "password": "admin123"})
        if response.status_code == 200:
            print("   ✅ Admin login working")
            
            # Test protected endpoint
            token = response.json()['access_token']
            headers = {"Authorization": f"Bearer {token}"}
            protected = requests.get("http://127.0.0.1:5000/api/v1/auth/protected", headers=headers)
            
            if protected.status_code == 200:
                data = protected.json()
                is_admin = data.get('is_admin', False)
                print(f"   ✅ Admin privileges: {is_admin}")
            else:
                print("   ⚠️  Protected endpoint issues")
        else:
            print(f"   ❌ Admin login failed: {response.status_code}")
    except:
        print("   ❌ Authentication system unavailable")
    
    # 4. Check relationships
    print("\n4. Relationships:")
    try:
        response = requests.get("http://127.0.0.1:5000/api/v1/places/")
        if response.status_code == 200:
            places = response.json()
            print(f"   ✅ {len(places)} places available")
            
            if places:
                # Test place details
                place_id = places[0]['id']
                detail_response = requests.get(f"http://127.0.0.1:5000/api/v1/places/{place_id}")
                
                if detail_response.status_code == 200:
                    place = detail_response.json()
                    has_owner = 'owner' in place
                    has_amenities = 'amenities' in place
                    print(f"   ✅ Relationships: Owner={has_owner}, Amenities={has_amenities}")
                else:
                    print("   ⚠️  Place details unavailable")
        else:
            print(f"   ❌ Places endpoint failed: {response.status_code}")
    except:
        print("   ❌ Relationships testing unavailable")
    
    print("\n" + "=" * 30)
    print("✅ Quick check complete!")
    print("\n💡 Next steps:")
    print("   - If server not running: python run.py")
    print("   - For full test: python comprehensive_test_suite.py")
    print("   - For detailed DB check: python explore_db.py")

if __name__ == "__main__":
    quick_check()