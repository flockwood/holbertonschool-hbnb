#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Admin User Script
Creates an admin user for the HBnB application.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_admin_user():
    """Create an admin user for the HBnB application."""
    try:
        from app.services.facade import HBnBFacade
        
        facade = HBnBFacade()
        
        # Admin user data
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@hbnb.com',
            'password': 'admin123'
        }
        
        print("Creating admin user...")
        print(f"Email: {admin_data['email']}")
        print(f"Password: {admin_data['password']}")
        
        try:
            # Try to create the admin user
            admin_user = facade.create_user(admin_data)
            # Make them admin
            admin_user.is_admin = True
            print(f"✅ Admin user created successfully!")
            print(f"   User ID: {admin_user.id}")
            print(f"   Admin Status: {admin_user.is_admin}")
            return admin_user
            
        except ValueError as e:
            if "already registered" in str(e):
                # User exists, promote to admin
                print("User already exists, promoting to admin...")
                existing_user = facade.get_user_by_email(admin_data['email'])
                if existing_user:
                    existing_user.is_admin = True
                    print(f"✅ Existing user promoted to admin!")
                    print(f"   User ID: {existing_user.id}")
                    print(f"   Admin Status: {existing_user.is_admin}")
                    return existing_user
                else:
                    print("❌ Could not find existing user")
                    return None
            else:
                print(f"❌ Error creating admin user: {e}")
                return None
                
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the correct directory.")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def main():
    """Main function."""
    print("=" * 50)
    print("HBnB Admin User Creation Script")
    print("=" * 50)
    
    admin_user = create_admin_user()
    
    if admin_user:
        print("\n" + "=" * 50)
        print("SUCCESS! Admin user is ready.")
        print("You can now login with:")
        print("  Email: admin@hbnb.com")
        print("  Password: admin123")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("FAILED! Could not create admin user.")
        print("=" * 50)
        sys.exit(1)

if __name__ == "__main__":
    main()