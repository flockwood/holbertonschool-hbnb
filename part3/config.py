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
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Shorter expiry in production
    
    def __init__(self):
        # Only check environment variables when this config is actually used
        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            raise ValueError("SECRET_KEY environment variable must be set in production")
        
        self.SECRET_KEY = secret_key
        self.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secret_key)

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