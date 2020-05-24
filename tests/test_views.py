from unittest import TestCase
from models import db, UserSearch, User, Appliance
import datetime
import os
from flask import session

os.environ['DATABASE_URL'] = "postgresql:///energy-test"
from app import app, login_manager


app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

class LoggedInViewTests(TestCase):

    @login_manager.request_loader
    def load_user_from_request(request):
        user = User.query.first()
        return user

    def setUp(self):
        User.query.delete()
        #clear database
        db.session.close()
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                email="test@test.com",
                                password="testuser")

        self.testuser_id = 4567
        self.testuser.id = self.testuser_id

        self.blender = Appliance(name="Blender",
                                watts=600,
                                category="Kitchen")

        self.blender_id = 1
        self.blender.id = self.blender_id
        db.session.add_all([self.testuser, self.blender])
        db.session.commit()
    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_successful_login_view(self):
        with self.client as c:
            resp = c.post('/login', data={
                'username': 'testuser',
                'password': 'testuser'
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Hello, testuser!', str(resp.data))

    def test_invalid_login_view(self):
        with self.client as c:
            resp = c.post('/login', data={
                'username': 'testtest',
                'password': 'password'
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Invalid login credentials. Please try again', str(resp.data))
    
    def test_save_auth(self):
        with self.client as c:
            with self.client.session_transaction() as sess:
                sess['search_key'] = [{'user_id': 4567, 'daily_kWh': 12.0, 'annual_consump': 144.0, 'annual_cost': '$16.92', 'freq': '300', 'ba': 'ERCOT_NORTH', 'percent': 71, 'point_time': '2020-05-24T18:20:00Z', 'appliance_id': 1, 'date': datetime.datetime(2020, 5, 24, 13, 22, 32, 226255), 'appliance_name': 'Blender', 'city': 'Denton', 'state': 'Texas'}]
            resp = c.post('/save', data=sess, follow_redirects=True)
           
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Annual Cost: $16.92', str(resp.data))
            self.assertIn('Location: Denton, Texas', str(resp.data))

class RegistrationViewsTest(TestCase):

    def setUp(self):
        db.session.close()
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    def test_valid_registration(self):
        self.client = app.test_client()
        with self.client as c:
            resp = c.post('/signup', data={
                'username': 'NewPerson', 'email': 'tester@tester.com', 'password': 'passiepassie'
            }, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Welcome to EnergyGuide, NewPerson', str(resp.data))
    

class AnonymousTestViews(TestCase):
    def setUp(self):
        db.session.close()
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_login_view(self):
        with self.client as c:
            resp = c.get('/login')
            self.assertIn('Username', str(resp.data))
            self.assertIn('Password', str(resp.data))

    def test_addappliance_unauth(self):
        with self.client as c:
            resp = c.get('/addappliance', follow_redirects=True)
            self.assertEqual(resp.status_code, 401)
            self.assertIn('Please log in to see this page', str(resp.data))

    def test_save_unauth(self):
        with self.client as c:
            resp = c.get('/save')
            self.assertEqual(resp.status_code, 405)

