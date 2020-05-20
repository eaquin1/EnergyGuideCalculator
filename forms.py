from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, BooleanField
from wtforms.validators import NumberRange, Length
from wtforms_components import SelectField, IntegerField, Email

class AddApplianceForm(FlaskForm):
    """Form for appliance energy calculator"""
    
    appliance = SelectField('My appliance')
    watts = IntegerField('Wattage')
    rate = IntegerField('Utility Rate, ¢/kWh')
    hours = IntegerField('Hours used per day', validators=[NumberRange(min=1, max=24)])
    days = IntegerField('Days used per year', validators=[NumberRange(min=1, max=365)])
    zipcode = StringField('Zip or Postal Code')
    
class NewUserForm(FlaskForm):
    """Form for a new user"""

    username = StringField('Username')
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginUserForm(FlaskForm):
    """Form for logging in user"""

    username = StringField('Username')
    password = PasswordField('Password', validators=[Length(min=6)])
    remember = BooleanField('Remember Me')


