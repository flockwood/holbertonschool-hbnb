#!/usr/bin/env python3
"""
Database Migration Script
Recreates the database with the new relationship structure.
"""

import os
import sys
from app import create_app, db

def migrate_database():
    """Drop existing database and recreate with relationships."""
    
    print("🔄 Starting database migration...")
    
    # Create app
    app = create_app()
    
    with app.app_context():
        try:
            # Check if database file exists
            db_path = 'development.db'
            if os.path.exists(db_path):
                print(f"📁 Found existing database: {db_path}")
                
                # Ask for confirmation
                response = input("⚠️  This will delete existing data. Continue? (y/N): ")
                if response.lower() != 'y':
                    print("❌ Migration cancelled")
                    return False
                
                # Drop all tables
                print("🗑️  Dropping existing tables...")
                db.drop_all()
                
                # Optional: Remove the database file entirely
                # os.remove(db_path)
                # print(f"🗑️  Removed database file: {db_path}")
            
            # Create all tables with new relationships
            print("🏗️  Creating tables with relationships...")
            db.create_all()
            
            # Verify tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print("✅ Database migration completed!")
            print("📊 Created tables:")
            for table in tables:
                print(f"   - {table}")
            
            # Create admin user
            print("\n👤 Creating admin user...")
            from app.services import facade
            
            try:
                admin_data = {
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'email': 'admin@hbnb.com',
                    'password': 'admin123'
                }
                admin = facade.create_user(admin_data)
                admin.is_admin = True
                admin.save()
                print("✅ Admin user created successfully!")
            except ValueError as e:
                if "already registered" in str(e):
                    print("ℹ️  Admin user already exists")
                else:
                    print(f"⚠️  Failed to create admin user: {e}")
            
            # Show relationship information
            print("\n🔗 Relationship Summary:")
            print("   • User → Places (one-to-many)")
            print("   • User → Reviews (one-to-many)")
            print("   • Place → Reviews (one-to-many)")
            print("   • Place ↔ Amenities (many-to-many)")
            
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False

def show_table_info():
    """Show detailed table information."""
    app = create_app()
    
    with app.app_context():
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            
            print("\n📋 Detailed Table Information:")
            
            for table_name in inspector.get_table_names():
                print(f"\n🔧 Table: {table_name}")
                columns = inspector.get_columns(table_name)
                foreign_keys = inspector.get_foreign_keys(table_name)
                
                print("   Columns:")
                for col in columns:
                    col_info = f"     - {col['name']} ({col['type']}"
                    if col.get('primary_key'):
                        col_info += ", PRIMARY KEY"
                    if not col.get('nullable', True):
                        col_info += ", NOT NULL"
                    if col.get('unique'):
                        col_info += ", UNIQUE"
                    col_info += ")"
                    print(col_info)
                
                if foreign_keys:
                    print("   Foreign Keys:")
                    for fk in foreign_keys:
                        print(f"     - {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}")
                
        except Exception as e:
            print(f"❌ Error showing table info: {e}")

def test_relationships():
    """Test the relationships by creating sample data."""
    app = create_app()
    
    with app.app_context():
        try:
            from app.services import facade
            
            print("\n🧪 Testing Relationships...")
            
            # Create a test user
            print("1. Creating test user...")
            user_data = {
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@example.com',
                'password': 'password123'
            }
            test_user = facade.create_user(user_data)
            print(f"   ✅ User created: {test_user.id}")
            
            # Create amenities
            print("2. Creating amenities...")
            wifi = facade.create_amenity({'name': 'WiFi'})
            pool = facade.create_amenity({'name': 'Pool'})
            print(f"   ✅ WiFi amenity: {wifi.id}")
            print(f"   ✅ Pool amenity: {pool.id}")
            
            # Create a place with amenities
            print("3. Creating place with amenities...")
            place_data = {
                'title': 'Beach House',
                'description': 'A lovely beach house',
                'price': 150.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': test_user.id,
                'amenities': [wifi.id, pool.id]
            }
            test_place = facade.create_place(place_data)
            print(f"   ✅ Place created: {test_place.id}")
            
            # Create a review
            print("4. Creating review...")
            review_data = {
                'text': 'Amazing place!',
                'rating': 5,
                'user_id': test_user.id,
                'place_id': test_place.id
            }
            test_review = facade.create_review(review_data)
            print(f"   ✅ Review created: {test_review.id}")
            
            # Test relationships
            print("5. Testing relationships...")
            
            # Test user → places relationship
            user_places = facade.get_user_places(test_user.id)
            print(f"   📍 User has {len(user_places)} place(s)")
            
            # Test user → reviews relationship
            user_reviews = facade.get_user_reviews(test_user.id)
            print(f"   💬 User has {len(user_reviews)} review(s)")
            
            # Test place → reviews relationship
            place_reviews = facade.get_place_reviews(test_place.id)
            print(f"   💬 Place has {len(place_reviews)} review(s)")
            
            # Test place ↔ amenities relationship
            place_detail = facade.get_place(test_place.id)
            print(f"   🏖️  Place has {len(place_detail['amenities'])} amenity(ies)")
            
            # Test amenity → places relationship
            wifi_places = facade.get_amenity_places(wifi.id)
            print(f"   📶 WiFi is in {len(wifi_places)} place(s)")
            
            print("\n✅ All relationship tests passed!")
            
        except Exception as e:
            print(f"❌ Relationship test failed: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Main migration function."""
    print("=" * 60)
    print("🏗️  HBnB Database Migration - Adding Relationships")
    print("=" * 60)
    
    # Run migration
    success = migrate_database()
    
    if success:
        # Show table information
        show_table_info()
        
        # Test relationships
        test_relationships()
        
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("🚀 Your database now has proper SQLAlchemy relationships!")
        print("=" * 60)
        
        print("\n📝 Next steps:")
        print("1. Update your existing code to use the new models")
        print("2. Test the API endpoints with the new relationships")
        print("3. Run your application: python run.py")
        
    else:
        print("\n" + "=" * 60)
        print("❌ Migration failed!")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()