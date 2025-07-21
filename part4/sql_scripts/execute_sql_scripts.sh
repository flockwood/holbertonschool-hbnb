#!/bin/bash

# HBnB Database Setup Script
# Executes all SQL scripts to create and test the database

echo "🗄️  HBnB DATABASE SETUP"
echo "========================"

# Database file name
DB_FILE="hbnb_raw_sql.db"

# Check if SQLite is installed
if ! command -v sqlite3 &> /dev/null; then
    echo "❌ SQLite3 is not installed. Please install it first:"
    echo "   Ubuntu/Debian: sudo apt install sqlite3"
    echo "   macOS: brew install sqlite3"
    echo "   Windows: Download from https://sqlite.org/download.html"
    exit 1
fi

echo "✅ SQLite3 found"

# Remove existing database if it exists
if [ -f "$DB_FILE" ]; then
    echo "🗑️  Removing existing database: $DB_FILE"
    rm "$DB_FILE"
fi

# Step 1: Create tables
echo ""
echo "📊 Step 1: Creating database schema..."
echo "======================================="
sqlite3 "$DB_FILE" < create_tables.sql

if [ $? -eq 0 ]; then
    echo "✅ Database schema created successfully"
else
    echo "❌ Failed to create database schema"
    exit 1
fi

# Step 2: Insert initial data
echo ""
echo "📝 Step 2: Inserting initial data..."
echo "===================================="
sqlite3 "$DB_FILE" < insert_initial_data.sql

if [ $? -eq 0 ]; then
    echo "✅ Initial data inserted successfully"
else
    echo "❌ Failed to insert initial data"
    exit 1
fi

# Step 3: Run CRUD tests
echo ""
echo "🧪 Step 3: Running CRUD tests..."
echo "================================"
sqlite3 "$DB_FILE" < test_crud_operations.sql

if [ $? -eq 0 ]; then
    echo "✅ CRUD tests completed successfully"
else
    echo "❌ CRUD tests failed"
    exit 1
fi

# Step 4: Display database info
echo ""
echo "📋 Step 4: Database Information"
echo "==============================="

echo "Database file: $DB_FILE"
echo "Database size: $(du -h "$DB_FILE" | cut -f1)"

echo ""
echo "Tables created:"
sqlite3 "$DB_FILE" "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"

echo ""
echo "Table row counts:"
sqlite3 "$DB_FILE" "
SELECT 'users' as table_name, COUNT(*) as row_count FROM users
UNION ALL
SELECT 'places', COUNT(*) FROM places  
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'amenities', COUNT(*) FROM amenities
UNION ALL
SELECT 'place_amenity', COUNT(*) FROM place_amenity;
"

echo ""
echo "🎉 DATABASE SETUP COMPLETED!"
echo "============================="
echo ""
echo "📍 Your database is ready at: $DB_FILE"
echo ""
echo "🔧 Quick commands to explore:"
echo "   sqlite3 $DB_FILE"
echo "   .tables"
echo "   .schema users"
echo "   SELECT * FROM users;"
echo ""
echo "🚀 You can now:"
echo "   1. Connect your application to this database"
echo "   2. Run additional SQL queries"
echo "   3. Import this schema into other database systems"