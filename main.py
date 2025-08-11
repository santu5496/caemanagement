from app import app

# Initialize sample data on startup
with app.app_context():
    try:
        from models import initialize_sample_data
        initialize_sample_data()
    except Exception as e:
        app.logger.error(f"Error initializing sample data: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
