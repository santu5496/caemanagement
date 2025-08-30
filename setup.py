#!/usr/bin/env python3
"""
Setup script for Friendscars application.
Run this script to initialize the database and create admin user.
"""

import os
import sys
from app import app, db
from models import initialize_sample_data

def setup_database():
    """Initialize database and create tables."""
    print("Setting up Friendscars database...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Initialize sample data
            initialize_sample_data()
            db.session.commit()
            print("✓ Sample data and admin user created")
            print("✓ Admin credentials: username=abc, password=123")
            
            print("\n🎉 Setup completed successfully!")
            print("Your Friendscars application is ready to use.")
            
        except Exception as e:
            print(f"❌ Error during setup: {e}")
            sys.exit(1)

if __name__ == "__main__":
    setup_database()