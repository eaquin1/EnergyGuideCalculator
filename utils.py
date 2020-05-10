from app import db
from models import db, connect_db, Appliance
from collections import defaultdict

def get_categories():
    """Returns a dictionary of the appliances sorted by category"""
    all_appliances = Appliance.query.all()
    
    category_dict = defaultdict(list)

    for appl in all_appliances:
       category_dict[appl.category].append((appl.id, appl.name))
    
    return category_dict

def calculate_consumption(calc_dict):

    calculations = {
        # "daily_kWh": 0,
        # "annual_consump": 0,
        # "annual_cost": 0
    }

    calculations["daily_kWh"] = (calc_dict["watts"] * calc_dict["hours"]) / 1000
    calculations["annual_consump"] = calculations["daily_kWh"] * calc_dict["days"]
    calculations["annual_cost"] = calculations["annual_consump"] * calc_dict["rate"]

    return calculations