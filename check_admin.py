
import os
import sys
sys.path.insert(0, os.getcwd())

# Set up Flask app context
os.environ["DATABASE_URL"] = "sqlite:///automarket.db"

from app import app, db
from models import AdminUser

with app.app_context():
    admin = AdminUser.query.filter_by(username="Friendscars").first()
    if admin:
        print(f"Admin user found: {admin.username}")
        print(f"Password check test: {admin.check_password("Friendscars@54961828")}")
    else:
        print("No admin user found with username Friendscars")
        
    # List all admin users
    all_admins = AdminUser.query.all()
    print(f"All admin users: {[u.username for u in all_admins]}")
