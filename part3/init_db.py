#!/usr/bin/env python3
"""Initialize the database and create tables."""

from app import create_app, db

def init_database():
    """Initialize the database and create all tables."""
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database initialized successfully!")
            print("✅ Tables created:")
            
            # Show created tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            for table in tables:
                print(f"   - {table}")
                
        except Exception as e:
            print(f"❌ Error initializing database: {e}")

if __name__ == "__main__":
    init_database()
    