from app import create_app

# Test with default config
app = create_app()
print(f"Debug mode: {app.config['DEBUG']}")
print(f"Secret key set: {'SECRET_KEY' in app.config}")

# Test with specific config
app_prod = create_app("config.Config")  # Production config
print(f"Production debug: {app_prod.config['DEBUG']}")