from app.services.facade import HBnBFacade

def debug_admin():
    facade = HBnBFacade()
    
    # Check if admin user exists
    admin_user = facade.get_user_by_email('admin@hbnb.com')
    
    if admin_user:
        print(f"✅ Admin user found: {admin_user.id}")
        print(f"   Email: {admin_user.email}")
        print(f"   Is Admin: {admin_user.is_admin}")
        print(f"   Has password hash: {hasattr(admin_user, 'password')}")
        
        # Test password verification
        try:
            password_valid = admin_user.verify_password('admin123')
            print(f"   Password verification: {password_valid}")
        except Exception as e:
            print(f"   Password verification error: {e}")
            
        # Check what attributes the user has
        print(f"   User attributes: {[attr for attr in dir(admin_user) if not attr.startswith('_')]}")
        
    else:
        print("❌ Admin user not found")

if __name__ == "__main__":
    debug_admin()