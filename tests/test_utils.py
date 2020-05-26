from unittest import TestCase
from models import Appliance, Utility
from utils import *
import os

os.environ['DATABASE_URL'] = "postgresql:///energy-test"

from app import app

db.create_all()

class UtilTests(TestCase):
    
    def setUp(self):
        #clear database
        
        db.drop_all()
        db.create_all()
        self.client = app.test_client()
        
        #create user
        blender = Appliance(name="Blender", watts=600, category="Kitchen")
        oven = Appliance(name="Oven", watts=3000, category="Kitchen")
        bulb = Appliance(name="Light bulb", watts=60, category="Lighting")
        hair_dryer = Appliance(name="Hair dryer", watts=300, category="Bathroom")
        tv = Appliance(name="Tv", watts=200, category="Home Electronics")
        dryer = Appliance(name="Dryer", watts=4000, category="Laundry")
        blender.id = 1
        oven.id = 2
        bulb.id = 3
        hair_dryer.id = 4
        tv.id = 5
        dryer.id = 6
        
        db.session.add_all([blender, oven, bulb, hair_dryer, tv, dryer])
        db.session.commit()
    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_get_appliances(self):
        appliances = get_appliances()
        choices = [('Kitchen', (
            (1, 'Blender'),
            (2, 'Oven')
        )),
        ('Lighting', ((3, 'Light bulb'),)),
        ('Bathroom', ((4, 'Hair dryer'), )),
        ('Home Electronics', ((5, 'Tv'), )), 
        ('Laundry', ((6, 'Dryer'), ))]
        self.assertEqual(appliances, choices)

    def test_get_categories(self):
        categories = get_categories()
        lst_cats = [('Bathroom', 'Bathroom'), ('Home Electronics', 'Home Electronics'), ('Kitchen', 'Kitchen'), ('Laundry', 'Laundry'), ('Lighting', 'Lighting')]
        self.assertEqual(categories, lst_cats)

    def test_consumption(self):

       watts = 203
       hours = 23
       days = 205
       rate = 15

       calc = calculate_consumption(watts, hours, days, rate)

       self.assertEqual(calc["daily_kWh"], 4.669)
       self.assertEqual(calc["annual_consump"], 957.1449999999999)
       self.assertEqual(calc["annual_cost"], '$143.57') 
       self.assertIsInstance(calc, dict)
