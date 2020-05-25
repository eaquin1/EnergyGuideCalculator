from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, BooleanField, IntegerField
from wtforms.validators import NumberRange, Length, InputRequired, ValidationError
from wtforms_components import SelectField, Email



class EnergySearchForm(FlaskForm):
    """Form for appliance energy calculator"""
    
    appliance = SelectField('My appliance', coerce=int)
    watts = IntegerField('Wattage', validators=[InputRequired()])
    rate = FloatField('Utility Rate, ¢/kWh', validators=[InputRequired()])
    hours = IntegerField('Hours used per day', validators=[NumberRange(min=1, max=24, message="Please enter 24 hours or less"), InputRequired()])
    days = IntegerField('Days used per year', validators=[NumberRange(min=1, max=365, message="Please enter 365 or less"), InputRequired()])
    zipcode = StringField('Zip or Postal Code', validators=[InputRequired()])
    

class NewUserForm(FlaskForm):
    """Form for a new user"""

    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[Email(), InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6), InputRequired()])

class LoginUserForm(FlaskForm):
    """Form for logging in user"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6), InputRequired()])
    remember = BooleanField('Remember Me')

class NewApplianceForm(FlaskForm):
    """Form to add new appliance"""

    name = StringField('Appliance', validators=[InputRequired()])
    watts = IntegerField('Watts', validators=[InputRequired()])
    category = SelectField('Category')

class EditUserForm(FlaskForm):
    """Form to edit user"""

    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[Email(), InputRequired()])

