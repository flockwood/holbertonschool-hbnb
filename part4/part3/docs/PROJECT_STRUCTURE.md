# HBnB Project Structure

## 📁 Directory Organization

```
part3/
├── app/                         # Core application
│   ├── api/v1/                 # API endpoints
│   ├── models/                 # SQLAlchemy models
│   ├── persistence/            # Data access layer
│   └── services/               # Business logic
├── tests/                      # All test files
│   ├── __init__.py            # Test package init
│   ├── conftest.py            # pytest configuration
│   ├── run_all_tests.py       # Master test runner
│   ├── quick_system_check.py  # Quick health check
│   ├── comprehensive_test_suite.py # Full system test
│   └── *.py                   # Other test files
├── scripts/                    # Management scripts
│   ├── migration_script.py    # Database migration
│   ├── create_admin.py        # Admin user creation
│   └── *.py                   # Other utility scripts
├── utils/                      # Utility functions
│   ├── generate_password_hash.py # Password utilities
│   ├── explore_db.py          # Database exploration
│   └── *.py                   # Other utilities
├── docs/                       # Documentation
│   ├── database/              # Database documentation
│   ├── api/                   # API documentation
│   └── diagrams/              # ER diagrams and visuals
├── sql_scripts/               # Raw SQL implementation
├── instance/                  # Flask instance folder
├── config.py                  # App configuration
├── run.py                     # Application entry point
├── requirements.txt           # Dependencies
└── README.md                  # Project documentation
```

## 🎯 Usage

### Running Tests
```bash
# Quick health check
python tests/quick_system_check.py

# Comprehensive testing
python tests/comprehensive_test_suite.py

# Run all tests
python tests/run_all_tests.py
```

### Scripts
```bash
# Database migration
python scripts/migration_script.py

# Create admin user
python scripts/create_admin.py
```

### Utilities
```bash
# Explore database
python utils/explore_db.py

# Generate password hash
python utils/generate_password_hash.py
```
