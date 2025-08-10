import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# In-memory storage for MVP
vehicles = {}
admin_users = {
    'admin': {
        'username': 'admin',
        'password_hash': generate_password_hash('admin123'),
        'created_at': datetime.now()
    }
}

# Add some sample vehicles for demonstration
def initialize_sample_data():
    if not vehicles:  # Only add if no vehicles exist
        sample_vehicles = [
            Vehicle(
                title="2020 Honda Civic LX",
                category="Cars",
                make="Honda",
                model="Civic",
                year=2020,
                price=18500,
                mileage=45000,
                description="Excellent condition, one owner, clean carfax. Great fuel economy and reliability.",
                contact_name="Auto Dealership",
                contact_phone="(555) 123-4567"
            ),
            Vehicle(
                title="2019 Ford F-150 XLT",
                category="Trucks",
                make="Ford",
                model="F-150",
                year=2019,
                price=32900,
                mileage=68000,
                description="4WD, crew cab, powerful V6 engine. Perfect for work and family use.",
                contact_name="Auto Dealership", 
                contact_phone="(555) 123-4567"
            ),
            Vehicle(
                title="2021 Toyota Camry LE",
                category="Cars",
                make="Toyota",
                model="Camry",
                year=2021,
                price=24800,
                mileage=28000,
                description="Low mileage, excellent condition. Advanced safety features included.",
                contact_name="Auto Dealership",
                contact_phone="(555) 123-4567"
            )
        ]
        
        for vehicle in sample_vehicles:
            add_vehicle(vehicle)

class Vehicle:
    def __init__(self, title, category, make, model, year, price, mileage, 
                 description, contact_name, contact_phone, images=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.category = category  # Cars, Trucks, Commercial Vehicles
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.mileage = mileage
        self.description = description
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.images = images or []
        self.status = 'available'  # available, sold
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'price': self.price,
            'mileage': self.mileage,
            'description': self.description,
            'contact_name': self.contact_name,
            'contact_phone': self.contact_phone,
            'images': self.images,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

def get_vehicle(vehicle_id):
    return vehicles.get(vehicle_id)

def get_all_vehicles():
    return list(vehicles.values())

def get_vehicles_by_category(category):
    return [v for v in vehicles.values() if v.category == category]

def get_available_vehicles():
    return [v for v in vehicles.values() if v.status == 'available']

def add_vehicle(vehicle):
    vehicles[vehicle.id] = vehicle
    return vehicle

def delete_vehicle(vehicle_id):
    if vehicle_id in vehicles:
        del vehicles[vehicle_id]
        return True
    return False

def verify_admin(username, password):
    user = admin_users.get(username)
    if user and check_password_hash(user['password_hash'], password):
        return True
    return False
