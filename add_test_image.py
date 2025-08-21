
#!/usr/bin/env python3

import sys
sys.path.append('.')

from app import app, db
from models import Vehicle

def add_image_to_vehicle():
    with app.app_context():
        # Find a vehicle without images
        vehicle = Vehicle.query.filter_by(images='').first()
        if not vehicle:
            vehicle = Vehicle.query.filter_by(images=None).first()
        
        if vehicle:
            print(f"Found vehicle without images: {vehicle.title} (ID: {vehicle.id})")
            # Add the test image
            vehicle.images = 'test_car_image.jpg'
            db.session.commit()
            print(f"Successfully added test_car_image.jpg to vehicle: {vehicle.title}")
            
            # Verify the update
            updated_vehicle = Vehicle.query.get(vehicle.id)
            print(f"Verification - Vehicle images: {updated_vehicle.images_list}")
        else:
            print("No vehicles found without images")

if __name__ == "__main__":
    add_image_to_vehicle()
