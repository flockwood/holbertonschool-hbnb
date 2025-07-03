from app import create_app

# Create app with default development configuration
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)