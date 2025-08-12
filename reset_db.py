
#!/usr/bin/env python3
"""Reset database and add sample vehicles"""

from app import app, db
from models import initialize_sample_data

def reset_database():
    """Reset the database and add sample data"""
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Add sample data including the new vehicles
        initialize_sample_data()
        
        print("✅ Database reset complete!")
        print("✅ Sample vehicles added including:")
        print("   - 2022 BMW 330i xDrive Sport Package (3 images)")
        print("   - 2023 Mercedes-Benz C300 4MATIC (3 images)")
        print("   - 2021 Audi A4 Prestige Quattro (3 images)")

if __name__ == "__main__":
    reset_database()
