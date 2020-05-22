from app import db
from models import db, connect_db, Appliance, Utility
from collections import defaultdict

def get_appliances():
    """Returns a list of tuples, of the appliances sorted by category
    [('Kitchen', (
        (1, 'Coffee Maker'),
        (2, 'Microwave Oven'),
        (3, 'Toaster Oven'),
        (39, 'Range Oven'),
        (40, 'Dishwasher'),
        (41, 'Refrigerator'))),
    ('Lighting': (
        (4, '18-W Compact Fluorescent'),
        (5, '60-W Incandescent Lamp'),
        (6, '100-W Incandescent Lamp'),
        (7, 'Torchiere Lamp-Halogen')],
    ('Bedroom and Bathroom': (
        (8, 'Hair Dryer'),
        (9, 'Waterbed Heater'))), ...]"""

    all_appliances = Appliance.query.all()
    
    category_dict = defaultdict(list)

    for appl in all_appliances:
       category_dict[appl.category].append((appl.id, appl.name))

    category_choices = [(cat, tuple(val)) for (cat, val) in category_dict.items()]    
    
    return category_choices

def get_categories():
    all_categories = [(val.category, val.category) for val in Appliance.query.distinct(Appliance.category)]
    return all_categories



def get_utility_rates():
    """Returns a list of tuples, of the utility rates sorted by location
    [('US Average Rate', (
        (12.79, 12.79))),
    ('Middle Atlantic', (
        (15.41, 15.41))),
    ('New Jersey', (
        (15.43, 15.43))))..."""

    all_rates = Utility.query.all()

    rate_dict = defaultdict(list)
    for rate in all_rates:
       rate_dict[rate.location].append((rate.id, rate.rate))

    rate_choices =[(cat, tuple(val)) for (cat, val) in rate_dict.items()] 

    return rate_choices

def calculate_consumption(watts, hours, days, rate):
    """Returns a dictionary of calculated energy costs
        { "daily_kWh": 5.7, "annual_consump": 5.7, "annual_cost": 0.69 }"""

    calculations = {}
    
    calculations["daily_kWh"] = (float(watts) * float(hours)) / 1000
    calculations["annual_consump"] = calculations["daily_kWh"] * float(days)
    calculations["annual_cost"] = calculations["annual_consump"] * (float(rate)/100)

    return calculations
