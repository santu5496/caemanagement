from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class VehicleForm(FlaskForm):
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
    contact_name = StringField('Contact Name', validators=[DataRequired(), Length(max=100)])
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(max=20)])
    images = MultipleFileField('Vehicle Images', 
                              validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    status = SelectField('Status', 
                        choices=[('available', 'Available'), ('sold', 'Sold')],
                        validators=[DataRequired()])
