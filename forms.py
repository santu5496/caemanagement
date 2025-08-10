from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, PasswordField, EmailField
from wtforms.validators import DataRequired, NumberRange, Length, Optional, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class VehicleForm(FlaskForm):
    # Basic Information
    title = StringField('Vehicle Title', validators=[DataRequired(), Length(min=5, max=100)])
    category = SelectField('Category', 
                          choices=[('Cars', 'Cars'), ('Trucks', 'Trucks'), ('Commercial Vehicles', 'Commercial Vehicles')],
                          validators=[DataRequired()])
    make = StringField('Make', validators=[DataRequired(), Length(max=50)])
    model = StringField('Model', validators=[DataRequired(), Length(max=50)])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1990, max=2025)])
    price = FloatField('Price ($)', validators=[DataRequired(), NumberRange(min=0)])
    mileage = IntegerField('Mileage (miles)', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description', validators=[Length(max=1000)])
    status = SelectField('Status', 
                        choices=[('available', 'Available'), ('sold', 'Sold')],
                        validators=[DataRequired()])
    
    # Engine & Performance
    fuel_type = SelectField('Fuel Type', 
                           choices=[('', 'Select Fuel Type'), ('Gasoline', 'Gasoline'), ('Diesel', 'Diesel'), 
                                   ('Hybrid', 'Hybrid'), ('Electric', 'Electric'), ('CNG', 'CNG')],
                           validators=[Optional()])
    transmission = SelectField('Transmission', 
                              choices=[('', 'Select Transmission'), ('Manual', 'Manual'), ('Automatic', 'Automatic'), ('CVT', 'CVT')],
                              validators=[Optional()])
    engine_size = StringField('Engine Size (Optional - e.g., 2.0L, 3.5L V6)', validators=[Optional(), Length(max=20)])
    horsepower = IntegerField('Horsepower (Optional)', validators=[Optional(), NumberRange(min=0, max=2000)])
    fuel_economy = StringField('Fuel Economy (e.g., 25 city / 32 highway mpg)', validators=[Optional(), Length(max=30)])
    drivetrain = SelectField('Drivetrain (Optional)', 
                            choices=[('', 'Select Drivetrain'), ('FWD', 'Front-Wheel Drive'), ('RWD', 'Rear-Wheel Drive'), 
                                    ('AWD', 'All-Wheel Drive'), ('4WD', '4-Wheel Drive')],
                            validators=[Optional()])
    
    # Ownership & History
    number_of_owners = IntegerField('Number of Previous Owners', validators=[Optional(), NumberRange(min=0, max=20)])
    previous_owner_name = StringField('Previous Owner Name', validators=[Optional(), Length(max=100)])
    previous_owner_phone = StringField('Previous Owner Phone', validators=[Optional(), Length(max=20)])
    previous_owner_email = EmailField('Previous Owner Email', validators=[Optional(), Email(), Length(max=100)])
    odometer_reading = IntegerField('Odometer Reading (miles)', validators=[Optional(), NumberRange(min=0)])
    accident_history = TextAreaField('Accident History', validators=[Optional(), Length(max=1000)])
    service_records = TextAreaField('Service Records', validators=[Optional(), Length(max=1000)])
    
    # Insurance & Documentation
    insurance_company = StringField('Insurance Company', validators=[Optional(), Length(max=100)])
    insurance_policy_number = StringField('Insurance Policy Number', validators=[Optional(), Length(max=50)])
    insurance_expiry = StringField('Insurance Expiry (MM/DD/YYYY)', validators=[Optional(), Length(max=10)])
    registration_number = StringField('Registration Number', validators=[Optional(), Length(max=50)])
    vin_number = StringField('VIN Number (17 characters)', validators=[Optional(), Length(min=17, max=17)])
    
    # Additional Features & Condition (Optional)
    exterior_color = StringField('Exterior Color (Optional)', validators=[Optional(), Length(max=30)])
    interior_color = StringField('Interior Color (Optional)', validators=[Optional(), Length(max=30)])
    features = TextAreaField('Features (Optional - comma-separated)', validators=[Optional(), Length(max=1000)])
    condition_rating = SelectField('Condition Rating (Optional)', 
                                  choices=[('', 'Select Condition'), ('Excellent', 'Excellent'), ('Good', 'Good'), 
                                          ('Fair', 'Fair'), ('Poor', 'Poor')],
                                  validators=[Optional()])
    warranty_info = TextAreaField('Warranty Information (Optional)', validators=[Optional(), Length(max=500)])
    
    # Contact & Images
    contact_name = StringField('Contact Name', validators=[DataRequired(), Length(max=100)])
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(max=20)])
    images = MultipleFileField('Vehicle Images', 
                              validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
