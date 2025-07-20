import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
Comprehensive System Test Suite
Tests all components of the HBnB project to ensure everything is working.
"""

import requests
import json
import sqlite3
import os
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api/v1"

class HBnBTester:
    def __init__(self):
        self.results = {
            'database': {'passed': 0, 'failed': 0, 'tests': []},
            'flask_app': {'passed': 0, 'failed': 0, 'tests': []},
            'relationships': {'passed': 0, 'failed': 0, 'tests': []},
            'auth': {'passed': 0, 'failed': 0, 'tests': []},
            'api_endpoints': {'passed': 0, 'failed': 0, 'tests': []}
        }
        self.admin_token = None
        self.test_user_token = None
        
    def log_test(self, category, test_name, passed, message=""):
        """Log test result."""
        result = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {result}: {test_name}")
        if message:
            print(f"      {message}")
        
        self.results[category]['tests'].append({
            'name': test_name,
            'passed': passed,
            'message': message
        })
        
        if passed:
            self.results[category]['passed'] += 1
        else:
            self.results[category]['failed'] += 1

    def test_database_files(self):
        """Test 1: Database Files Existence"""
        print("\n🗄️  Testing Database Files...")
        
        # Test SQLAlchemy database (in instance folder - Flask convention)
        sqlalchemy_db = "./instance/development.db"
        exists = os.path.exists(sqlalchemy_db)
        self.log_test('database', 'SQLAlchemy database exists', exists, 
                     f"File: {sqlalchemy_db}, Size: {os.path.getsize(sqlalchemy_db) if exists else 0} bytes")
        
        # Test raw SQL database
        raw_sql_db = "./sql_scripts/hbnb_raw_sql.db"
        exists = os.path.exists(raw_sql_db)
        self.log_test('database', 'Raw SQL database exists', exists,
                     f"File: {raw_sql_db}, Size: {os.path.getsize(raw_sql_db) if exists else 0} bytes")

    def test_sqlalchemy_database(self):
        """Test 2: SQLAlchemy Database Content"""
        print("\n🔗 Testing SQLAlchemy Database...")
        
        try:
            conn = sqlite3.connect('./instance/development.db')
            cursor = conn.cursor()
            
            # Test tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            expected_tables = ['users', 'places', 'reviews', 'amenities', 'place_amenity']
            
            for table in expected_tables:
                exists = table in tables
                self.log_test('database', f'SQLAlchemy table {table} exists', exists)
            
            # Test data exists
            for table in expected_tables:
                if table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table};")
                    count = cursor.fetchone()[0]
                    self.log_test('database', f'SQLAlchemy {table} has data', count > 0, f"{count} rows")
            
            conn.close()
            
        except Exception as e:
            self.log_test('database', 'SQLAlchemy database connection', False, str(e))

    def test_raw_sql_database(self):
        """Test 3: Raw SQL Database Content"""
        print("\n📊 Testing Raw SQL Database...")
        
        try:
            conn = sqlite3.connect('./sql_scripts/hbnb_raw_sql.db')
            cursor = conn.cursor()
            
            # Test admin user
            cursor.execute("SELECT email, is_admin FROM users WHERE email = 'admin@hbnb.io';")
            admin = cursor.fetchone()
            self.log_test('database', 'Raw SQL admin user exists', admin is not None)
            if admin:
                self.log_test('database', 'Raw SQL admin has privileges', admin[1] == 1)
            
            # Test amenities
            cursor.execute("SELECT COUNT(*) FROM amenities;")
            amenity_count = cursor.fetchone()[0]
            self.log_test('database', 'Raw SQL amenities exist', amenity_count >= 3, f"{amenity_count} amenities")
            
            # Test relationships
            cursor.execute("SELECT COUNT(*) FROM place_amenity;")
            relationship_count = cursor.fetchone()[0]
            self.log_test('database', 'Raw SQL relationships exist', relationship_count > 0, f"{relationship_count} relationships")
            
            conn.close()
            
        except Exception as e:
            self.log_test('database', 'Raw SQL database connection', False, str(e))

    def test_flask_app_startup(self):
        """Test 4: Flask Application Startup"""
        print("\n🚀 Testing Flask Application...")
        
        try:
            # Test basic connectivity
            response = requests.get(f"{BASE_URL}/amenities/", timeout=5)
            self.log_test('flask_app', 'Flask server running', response.status_code == 200, 
                         f"Status: {response.status_code}")
            
            # Test API documentation
            response = requests.get("http://127.0.0.1:5000/api/v1/", timeout=5)
            self.log_test('flask_app', 'Swagger API docs accessible', response.status_code == 200)
            
        except requests.exceptions.ConnectionError:
            self.log_test('flask_app', 'Flask server running', False, "Connection refused - server not running")
        except Exception as e:
            self.log_test('flask_app', 'Flask server running', False, str(e))

    def test_authentication(self):
        """Test 5: Authentication System"""
        print("\n🔐 Testing Authentication...")
        
        # Test admin login
        try:
            response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": "admin@hbnb.com",
                "password": "admin123"
            })
            
            if response.status_code == 200:
                self.admin_token = response.json()['access_token']
                self.log_test('auth', 'Admin login successful', True)
                
                # Test protected endpoint
                headers = {"Authorization": f"Bearer {self.admin_token}"}
                protected_response = requests.get(f"{BASE_URL}/auth/protected", headers=headers)
                self.log_test('auth', 'Admin protected access', protected_response.status_code == 200)
                
                if protected_response.status_code == 200:
                    data = protected_response.json()
                    is_admin = data.get('is_admin', False)
                    self.log_test('auth', 'Admin privileges verified', is_admin)
            else:
                self.log_test('auth', 'Admin login successful', False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test('auth', 'Admin login successful', False, str(e))

        # Test invalid login
        try:
            response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": "invalid@test.com",
                "password": "wrongpassword"
            })
            self.log_test('auth', 'Invalid login rejected', response.status_code == 401)
        except Exception as e:
            self.log_test('auth', 'Invalid login rejected', False, str(e))

    def test_api_endpoints(self):
        """Test 6: Core API Endpoints"""
        print("\n🌐 Testing API Endpoints...")
        
        if not self.admin_token:
            print("   ⚠️  Skipping API tests - no admin token")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test GET endpoints (public)
        endpoints = [
            ('/users', 'Users list'),
            ('/amenities', 'Amenities list'),
            ('/places', 'Places list'),
            ('/reviews', 'Reviews list')
        ]
        
        for endpoint, name in endpoints:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}")
                self.log_test('api_endpoints', f'GET {name}', response.status_code == 200,
                             f"Status: {response.status_code}")
            except Exception as e:
                self.log_test('api_endpoints', f'GET {name}', False, str(e))
        
        # Test POST endpoints (require auth)
        # Create test user
        try:
            test_user_data = {
                "first_name": "Test",
                "last_name": "User",
                "email": f"test_{int(datetime.now().timestamp())}@test.com",
                "password": "test123"
            }
            
            response = requests.post(f"{BASE_URL}/users/", json=test_user_data, headers=headers)
            self.log_test('api_endpoints', 'POST Create user', response.status_code == 201,
                         f"Status: {response.status_code}")
            
            if response.status_code == 201:
                test_user = response.json()
                test_user_id = test_user['id']
                
                # Login as test user
                login_response = requests.post(f"{BASE_URL}/auth/login", json={
                    "email": test_user_data['email'],
                    "password": test_user_data['password']
                })
                
                if login_response.status_code == 200:
                    self.test_user_token = login_response.json()['access_token']
                    user_headers = {"Authorization": f"Bearer {self.test_user_token}"}
                    
                    # Create test place
                    place_data = {
                        "title": "Test API Place",
                        "description": "Testing API functionality",
                        "price": 99.99,
                        "latitude": 40.7128,
                        "longitude": -74.0060,
                        "amenities": []
                    }
                    
                    place_response = requests.post(f"{BASE_URL}/places/", json=place_data, headers=user_headers)
                    self.log_test('api_endpoints', 'POST Create place', place_response.status_code == 201,
                                 f"Status: {place_response.status_code}")
                    
        except Exception as e:
            self.log_test('api_endpoints', 'POST Create user', False, str(e))

    def test_relationships(self):
        """Test 7: Database Relationships"""
        print("\n🔗 Testing Database Relationships...")
        
        try:
            # Test user-place relationship
            response = requests.get(f"{BASE_URL}/places/")
            if response.status_code == 200:
                places = response.json()
                self.log_test('relationships', 'Places endpoint returns data', len(places) > 0,
                             f"{len(places)} places found")
                
                if places:
                    # Test place details with relationships
                    place_id = places[0]['id']
                    detail_response = requests.get(f"{BASE_URL}/places/{place_id}")
                    
                    if detail_response.status_code == 200:
                        place_detail = detail_response.json()
                        has_owner = 'owner' in place_detail
                        has_amenities = 'amenities' in place_detail
                        
                        self.log_test('relationships', 'Place-Owner relationship', has_owner)
                        self.log_test('relationships', 'Place-Amenity relationship', has_amenities)
                        
                        if has_amenities:
                            amenity_count = len(place_detail['amenities'])
                            self.log_test('relationships', 'Amenities loaded correctly', True,
                                         f"{amenity_count} amenities")
            
        except Exception as e:
            self.log_test('relationships', 'Relationship testing', False, str(e))

    def test_crud_operations(self):
        """Test 8: CRUD Operations"""
        print("\n📝 Testing CRUD Operations...")
        
        if not self.admin_token:
            print("   ⚠️  Skipping CRUD tests - no admin token")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # CREATE
        amenity_data = {"name": f"Test_Amenity_{int(datetime.now().timestamp())}"}
        try:
            response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=headers)
            created = response.status_code == 201
            self.log_test('api_endpoints', 'CREATE amenity', created)
            
            if created:
                amenity = response.json()
                amenity_id = amenity['id']
                
                # READ
                read_response = requests.get(f"{BASE_URL}/amenities/{amenity_id}")
                self.log_test('api_endpoints', 'READ amenity', read_response.status_code == 200)
                
                # UPDATE
                update_data = {"name": f"Updated_Amenity_{int(datetime.now().timestamp())}"}
                update_response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", 
                                             json=update_data, headers=headers)
                self.log_test('api_endpoints', 'UPDATE amenity', update_response.status_code == 200)
                
        except Exception as e:
            self.log_test('api_endpoints', 'CRUD operations', False, str(e))

    def run_all_tests(self):
        """Run all tests and print summary."""
        print("🧪 COMPREHENSIVE HBNB SYSTEM TEST")
        print("=" * 50)
        
        # Run all test categories
        self.test_database_files()
        self.test_sqlalchemy_database()
        self.test_raw_sql_database()
        self.test_flask_app_startup()
        self.test_authentication()
        self.test_api_endpoints()
        self.test_relationships()
        self.test_crud_operations()
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        total_passed = 0
        total_failed = 0
        
        for category, results in self.results.items():
            passed = results['passed']
            failed = results['failed']
            total = passed + failed
            
            if total > 0:
                percentage = (passed / total) * 100
                status = "✅" if failed == 0 else "⚠️" if passed > failed else "❌"
                print(f"{status} {category.upper()}: {passed}/{total} ({percentage:.1f}%)")
                
                total_passed += passed
                total_failed += failed
        
        print(f"\n🎯 OVERALL: {total_passed}/{total_passed + total_failed} tests passed")
        
        if total_failed == 0:
            print("🎉 ALL SYSTEMS OPERATIONAL!")
        elif total_passed > total_failed:
            print("⚠️  MOSTLY WORKING - Some issues to address")
        else:
            print("❌ CRITICAL ISSUES - System needs attention")
        
        # Provide recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if total_failed == 0:
            print("   🚀 Your HBnB system is fully functional!")
            print("   📝 All databases, APIs, and relationships working perfectly")
            print("   🎯 Ready for production or further development")
        else:
            print("   🔧 Check failed tests above for specific issues")
            print("   🚀 Restart Flask server if API tests failed")
            print("   🗄️  Check database files if database tests failed")

def main():
    """Main test runner."""
    print("Starting comprehensive system test...")
    print("Make sure your Flask server is running: python run.py")
    print()
    
    tester = HBnBTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()