from app.services.facade import HBnBFacade

def create_admin_user():
    facade = HBnBFacade()
    
    # Create an admin user
    admin_data = {
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@hbnb.com',
        'password': 'admin123'
    }
    
    try:
        admin_user = facade.create_user(admin_data)
        # Make them admin
        admin_user.is_admin = True
        print(f"✅ Admin user created: {admin_user.id}")
        print(f"Email: {admin_user.email}")
        print(f"Password: admin123")
        return admin_user
    except ValueError as e:
        if "already registered" in str(e):
            # Get existing user and make admin
            existing_user = facade.get_user_by_email(admin_data['email'])
            existing_user.is_admin = True
            print(f"✅ Existing user promoted to admin: {existing_user.id}")
            return existing_user
        else:
            print(f"❌ Error: {e}")
            return None

if __name__ == "__main__":
    create_admin_user()
