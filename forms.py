from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms.validators import NumberRange
from wtforms_components import SelectField, IntegerField

class AddApplianceForm(FlaskForm):
    """Form for appliance energy calculator"""
    appliance = SelectField('My appliance', coerce=int)
    watts = IntegerField('Wattage')
    rate = SelectField('Utility Rate')
    hours = IntegerField('Hours used per day', validators=[NumberRange(min=1, max=24)])
    days = IntegerField('Days used per year', validators=[NumberRange(min=1, max=365)])
   # wtforms.widgets.ListWidget(html_tag='ul', prefix_label=True)