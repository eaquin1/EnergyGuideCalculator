from app import db
from models import db, connect_db, Appliance
from collections import defaultdict

def get_categories():
    """Returns a dictionary of the appliances sorted by category
    {'Kitchen': [(1, 'Coffee Maker'),
              (2, 'Microwave Oven'),
              (3, 'Toaster Oven'),
              (39, 'Range Oven'),
              (40, 'Dishwasher'),
              (41, 'Refrigerator')],
             'Lighting': [(4, '18-W Compact Fluorescent'),
              (5, '60-W Incandescent Lamp'),
              (6, '100-W Incandescent Lamp'),
              (7, 'Torchiere Lamp-Halogen')],
             'Bedroom and Bathroom': [(8, 'Hair Dryer'),
              (9, 'Waterbed Heater')], ..."""

    all_appliances = Appliance.query.all()
    
    category_dict = defaultdict(list)

    for appl in all_appliances:
       category_dict[appl.category].append((appl.id, appl.name))

    category_choices = [(cat, tuple(val)) for (cat, val) in category_dict.items()]    
    
    return category_choices

def calculate_consumption(calc_dict):
    """Returns a dictionary of calculated energy costs
        { "daily_kWh": 5.7, "annual_consump": 5.7, "annual_cost": 0.69 }"""

    calculations = {}
    
    calculations["daily_kWh"] = (calc_dict["watts"] * calc_dict["hours"]) / 1000
    calculations["annual_consump"] = calculations["daily_kWh"] * calc_dict["days"]
    calculations["annual_cost"] = calculations["annual_consump"] * calc_dict["rate"]

    return calculations