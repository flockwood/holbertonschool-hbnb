import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
"""
pytest configuration for HBnB tests.
"""

import pytest
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

@pytest.fixture(scope="session")
def app():
    """Create application for testing."""
    from app import create_app
    app = create_app()
    return app

@pytest.fixture(scope="session")
def client(app):
    """Create test client."""
    return app.test_client()
