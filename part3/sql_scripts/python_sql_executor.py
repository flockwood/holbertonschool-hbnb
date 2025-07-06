#!/usr/bin/env python3
"""
Python SQL Executor
Alternative to bash script for Windows users without sqlite3 command.
"""

import sqlite3
import os
import sys

def execute_sql_file(cursor, filename):
    """Execute SQL commands from a file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Remove comments and empty lines
        lines = []
        for line in sql_content.split('\n'):
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('--'):
                lines.append(line)
        
        # Join lines back together
        cleaned_sql = ' '.join(lines)
        
        # Use executescript for complex SQL with multiple statements
        cursor.executescript(cleaned_sql)
        
        return True
    except Exception as e:
        print(f"❌ Error executing {filename}: {e}")
        print(f"   Trying alternative parsing method...")
        
        # Alternative: try executing line by line for debugging
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            
            # Split by semicolon but be smarter about it
            statements = []
            current_statement = ""
            
            for line in sql_content.split('\n'):
                line = line.strip()
                if line and not line.startswith('--'):
                    current_statement += " " + line
                    if line.endswith(';'):
                        statements.append(current_statement.strip())
                        current_statement = ""
            
            # Execute each statement
            for i, statement in enumerate(statements):
                if statement and statement != ';':
                    try:
                        cursor.execute(statement)
                        print(f"   ✅ Executed statement {i+1}")
                    except Exception as stmt_error:
                        print(f"   ❌ Statement {i+1} failed: {stmt_error}")
                        print(f"   Statement: {statement[:100]}...")
                        return False
            
            return True
            
        except Exception as e2:
            print(f"❌ Alternative parsing also failed: {e2}")
            return False

def main():
    """Main execution function."""
    print("🗄️  HBnB DATABASE SETUP (Python Version)")
    print("==========================================")
    
    # Database file name
    db_file = "hbnb_raw_sql.db"
    
    # Remove existing database if it exists
    if os.path.exists(db_file):
        print(f"🗑️  Removing existing database: {db_file}")
        os.remove(db_file)
    
    # Connect to database (creates it if it doesn't exist)
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        print("✅ Database connection established")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return
    
    try:
        # Step 1: Create tables
        print("\n📊 Step 1: Creating database schema...")
        print("=======================================")
        
        if execute_sql_file(cursor, "create_tables.sql"):
            conn.commit()
            print("✅ Database schema created successfully")
        else:
            print("❌ Failed to create database schema")
            return
        
        # Step 2: Insert initial data
        print("\n📝 Step 2: Inserting initial data...")
        print("====================================")
        
        if execute_sql_file(cursor, "insert_initial_data.sql"):
            conn.commit()
            print("✅ Initial data inserted successfully")
        else:
            print("❌ Failed to insert initial data")
            return
        
        # Step 3: Run CRUD tests
        print("\n🧪 Step 3: Running CRUD tests...")
        print("================================")
        
        if execute_sql_file(cursor, "test_crud_operations.sql"):
            conn.commit()
            print("✅ CRUD tests completed successfully")
        else:
            print("❌ CRUD tests failed")
            return
        
        # Step 4: Display database info
        print("\n📋 Step 4: Database Information")
        print("===============================")
        
        print(f"Database file: {db_file}")
        print(f"Database size: {os.path.getsize(db_file)} bytes")
        
        print("\nTables created:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()
        for table in tables:
            print(f"  - {table[0]}")
        
        print("\nTable row counts:")
        count_queries = [
            ("users", "SELECT COUNT(*) FROM users"),
            ("places", "SELECT COUNT(*) FROM places"),
            ("reviews", "SELECT COUNT(*) FROM reviews"),
            ("amenities", "SELECT COUNT(*) FROM amenities"),
            ("place_amenity", "SELECT COUNT(*) FROM place_amenity")
        ]
        
        for table_name, query in count_queries:
            try:
                cursor.execute(query)
                count = cursor.fetchone()[0]
                print(f"  - {table_name}: {count} rows")
            except Exception as e:
                print(f"  - {table_name}: Error counting rows")
        
        print("\n🎉 DATABASE SETUP COMPLETED!")
        print("=============================")
        print(f"\n📍 Your database is ready at: {db_file}")
        print("\n🔧 You can now connect to it using:")
        print("   - Python sqlite3 module")
        print("   - DB Browser for SQLite")
        print("   - Any SQLite client")
        print("\n🚀 Example Python connection:")
        print("   import sqlite3")
        print(f"   conn = sqlite3.connect('{db_file}')")
        print("   cursor = conn.cursor()")
        print("   cursor.execute('SELECT * FROM users;')")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Close database connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()