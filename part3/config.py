import os
from datetime import timedelta

class Config:
    # Basic Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Tokens expire in 1 hour
    JWT_ALGORITHM = 'HS256'
    
    # Security settings
    DEBUG = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    # In development, you might want longer token expiry for testing
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

class ProductionConfig(Config):
    # Production settings - more secure
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Shorter expiry in production
    
    # Ensure required environment variables are set
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")
    
    if not JWT_SECRET_KEY:
        JWT_SECRET_KEY = SECRET_KEY

class TestConfig(Config):
    TESTING = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)  # Short expiry for tests

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}