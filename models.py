import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sqlalchemy import String, Integer, Float, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # Cars, Trucks, Commercial Vehicles
    make: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    contact_name: Mapped[str] = mapped_column(String(100), nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    contact_email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    images: Mapped[str] = mapped_column(Text)  # JSON string of image filenames
    status: Mapped[str] = mapped_column(String(20), default='available')  # available, sold
    
    # Comprehensive Vehicle Details
    # Engine & Performance
    fuel_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # Gasoline, Diesel, Hybrid, Electric
    transmission: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # Manual, Automatic, CVT
    engine_size: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # e.g. 2.0L, 3.5L V6
    horsepower: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    fuel_economy: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)  # e.g. 25 city / 32 highway mpg
    drivetrain: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # FWD, RWD, AWD, 4WD
    
    # Ownership & History
    number_of_owners: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    previous_owner_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    previous_owner_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    previous_owner_email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    odometer_reading: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Current odometer in miles/km
    accident_history: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Description of any accidents
    service_records: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Service history notes
    
    # Insurance & Documentation
    insurance_company: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    insurance_policy_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    insurance_expiry: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # MM/DD/YYYY
    registration_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    vin_number: Mapped[Optional[str]] = mapped_column(String(17), nullable=True)  # Vehicle Identification Number
    
    # Additional Features & Condition
    exterior_color: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    interior_color: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    features: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Comma-separated features
    condition_rating: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # Excellent, Good, Fair, Poor
    warranty_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Warranty details
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, title, category, make, model, year, price, mileage, 
                 description, contact_name, contact_phone, images=None, contact_email=None, **kwargs):
        self.id = str(uuid.uuid4())
        self.title = title
        self.category = category
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.mileage = mileage
        self.description = description
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.images = ','.join(images) if images else ''
        self.status = 'available'
        
        # Set additional attributes from kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def images_list(self):
        """Return images as a list"""
        return [img.strip() for img in self.images.split(',') if img.strip()] if self.images else []

    @images_list.setter
    def images_list(self, value):
        """Set images from a list"""
        self.images = ','.join(value) if value else ''
    
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
            'contact_email': self.contact_email,
            'images': self.images_list,
            'status': self.status,
            
            # Comprehensive details
            'fuel_type': self.fuel_type,
            'transmission': self.transmission,
            'engine_size': self.engine_size,
            'horsepower': self.horsepower,
            'fuel_economy': self.fuel_economy,
            'drivetrain': self.drivetrain,
            'number_of_owners': self.number_of_owners,
            'previous_owner_name': self.previous_owner_name,
            'previous_owner_phone': self.previous_owner_phone,
            'previous_owner_email': self.previous_owner_email,
            'odometer_reading': self.odometer_reading,
            'accident_history': self.accident_history,
            'service_records': self.service_records,
            'insurance_company': self.insurance_company,
            'insurance_policy_number': self.insurance_policy_number,
            'insurance_expiry': self.insurance_expiry,
            'registration_number': self.registration_number,
            'vin_number': self.vin_number,
            'exterior_color': self.exterior_color,
            'interior_color': self.interior_color,
            'features': self.features,
            'condition_rating': self.condition_rating,
            'warranty_info': self.warranty_info,
            
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def update_from_dict(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                if key == 'images' and isinstance(value, list):
                    self.images_list = value
                else:
                    setattr(self, key, value)
        self.updated_at = datetime.utcnow()

def initialize_sample_data():
    """Initialize sample data if database is empty"""
    # Check if admin user exists
    existing_admin = AdminUser.query.filter_by(username='admin').first()
    if existing_admin:
        # Remove old admin user
        db.session.delete(existing_admin)
    
    # Check if new admin user exists
    if not AdminUser.query.filter_by(username='Friendscars').first():
        admin = AdminUser()
        admin.username = 'Friendscars'
        admin.set_password('Friendscars@54961828')
        db.session.add(admin)
    
    # Check if sample vehicles exist
    if Vehicle.query.count() == 0:
        sample_vehicles = [
            Vehicle(
                title="2020 Honda Civic LX",
                category="Cars",
                make="Honda",
                model="Civic",
                year=2020,
                price=1550000,
                mileage=45000,
                description="Excellent condition, one owner, clean carfax. Great fuel economy and reliability.",
                contact_name="Friendscars",
                contact_phone="(555) 123-4567"
            ),
            Vehicle(
                title="2019 Ford F-150 XLT",
                category="Trucks",
                make="Ford",
                model="F-150",
                year=2019,
                price=2750000,
                mileage=68000,
                description="4WD, crew cab, powerful V6 engine. Perfect for work and family use.",
                contact_name="Friendscars", 
                contact_phone="(555) 123-4567"
            ),
            Vehicle(
                title="2021 Toyota Camry LE",
                category="Cars",
                make="Toyota",
                model="Camry",
                year=2021,
                price=2080000,
                mileage=28000,
                description="Low mileage, excellent condition. Advanced safety features included.",
                contact_name="Friendscars",
                contact_phone="(555) 123-4567"
            ),
            Vehicle(
                title="2022 BMW 330i xDrive Sport Package",
                category="Cars",
                make="BMW",
                model="330i",
                year=2022,
                price=3450000,
                mileage=18500,
                description="Luxury sports sedan with premium interior, advanced technology, and all-wheel drive. Meticulously maintained with full service history.",
                contact_name="Friendscars",
                contact_phone="(555) 123-4567",
                images=["bmw_330i_front.jpg", "bmw_330i_interior.jpg", "bmw_330i_side.jpg"],
                fuel_type="Gasoline",
                transmission="Automatic",
                engine_size="2.0L Turbo",
                horsepower=255,
                fuel_economy="26 city / 36 highway mpg",
                drivetrain="AWD",
                exterior_color="Mineral Grey Metallic",
                interior_color="Black Dakota Leather",
                features="Sport Package, Premium Package, Navigation, Sunroof, Heated Seats",
                condition_rating="Excellent",
                number_of_owners=1
            ),
            Vehicle(
                title="2023 Mercedes-Benz C300 4MATIC",
                category="Cars",
                make="Mercedes-Benz",
                model="C300",
                year=2023,
                price=4250000,
                mileage=8200,
                description="Nearly new luxury sedan with cutting-edge technology and refined performance. Under warranty with premium care package included.",
                contact_name="Friendscars",
                contact_phone="(555) 123-4567",
                images=["mercedes_c300_front.jpg", "mercedes_c300_interior.jpg", "mercedes_c300_rear.jpg"],
                fuel_type="Gasoline",
                transmission="Automatic",
                engine_size="2.0L Turbo",
                horsepower=255,
                fuel_economy="23 city / 32 highway mpg",
                drivetrain="AWD",
                exterior_color="Obsidian Black Metallic",
                interior_color="Macchiato Beige/Black MB-Tex",
                features="Premium Package, AMG Line, MBUX Infotainment, Burmester Audio, Panoramic Sunroof",
                condition_rating="Excellent",
                number_of_owners=1,
                warranty_info="Factory warranty until 2027 + Extended coverage"
            ),
            Vehicle(
                title="2021 Audi A4 Prestige Quattro",
                category="Cars",
                make="Audi",
                model="A4",
                year=2021,
                price=3780000,
                mileage=22100,
                description="Premium compact sedan with sophisticated design and advanced driver assistance features. Perfect blend of performance and comfort.",
                contact_name="Friendscars",
                contact_phone="(555) 123-4567",
                images=["audi_a4_front.jpg", "audi_a4_interior.jpg", "audi_a4_profile.jpg"],
                fuel_type="Gasoline",
                transmission="Automatic",
                engine_size="2.0L TFSI",
                horsepower=261,
                fuel_economy="24 city / 31 highway mpg",
                drivetrain="AWD",
                exterior_color="Glacier White Metallic",
                interior_color="Black Fine Nappa Leather",
                features="Prestige Package, Virtual Cockpit Plus, Bang & Olufsen Audio, Adaptive Cruise Control",
                condition_rating="Excellent",
                number_of_owners=1,
                service_records="Full Audi dealer maintenance history"
            )
        ]
        
        for vehicle in sample_vehicles:
            db.session.add(vehicle)
    
    db.session.commit()

# Helper functions for backward compatibility
def get_vehicle(vehicle_id):
    return Vehicle.query.get(vehicle_id)

def get_all_vehicles():
    return Vehicle.query.all()

def get_vehicles_by_category(category):
    return Vehicle.query.filter_by(category=category).all()

def get_available_vehicles():
    return Vehicle.query.filter_by(status='available').all()

def add_vehicle(vehicle):
    db.session.add(vehicle)
    db.session.commit()
    return vehicle

def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
        return True
    return False

def verify_admin(username, password):
    user = AdminUser.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return True
    return False
