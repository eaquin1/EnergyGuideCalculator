import os
from unittest import TestCase
from models import db, UserSearch, User, Appliance
from datetime import datetime
os.environ['DATABASE_URL'] = "postgresql:///energy-test"
from app import app

db.create_all()

class SearchTests(TestCase):

    def setUp(self):
        #clear database
        
        db.drop_all()
        db.create_all()
        self.client = app.test_client()
        #create search
        user12 = User(username="bob", email="bob@bob.com", password="something")
        user12.id = 12
        blender = Appliance(name="Blender", watts=300, category="kitchen")
        blender.id = 2
        db.session.add_all([user12, blender])
        db.session.commit()

        search = UserSearch(user_id=12, appliance_id=2, daily_kWh=12, annual_Consump=1440, annual_Cost="$169.20", timestamp=datetime(2020, 5, 23, 20, 21, 44), grid="ERCOT_NORTH", gridpercent=77, state="Texas", city="Denton")
        db.session.add(search)
        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_search_model(self):
        #should only be one search in the database
        search = UserSearch.query.first()
        all_searches = UserSearch.query.all()
        self.assertEqual(len(all_searches), 1)
        self.assertEqual(search.user_id, 12)
        self.assertEqual(search.annual_Cost, "$169.20")

    def test_friendly_date(self):
        search = UserSearch.query.first()
        self.assertEqual(search.friendly_date, "May 23 2020 08:21 PM")

