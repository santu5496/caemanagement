
#!/usr/bin/env python3
"""Clear all vehicles from the database"""

from app import app, db
from models import Vehicle

def clear_all_vehicles():
    """Remove all vehicles from the database"""
    with app.app_context():
        try:
            # Delete all vehicles
            deleted_count = Vehicle.query.count()
            Vehicle.query.delete()
            db.session.commit()
            
            print(f"✅ Successfully removed {deleted_count} vehicles from the database!")
            print("✅ Admin user remains intact for future use.")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error clearing vehicles: {e}")

if __name__ == "__main__":
    clear_all_vehicles()
