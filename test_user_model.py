"""User model tests"""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Appliance, UserSearch, Utility

os.environ['DATABASE_URL'] = "postgresql:///energy-test"

from app import app

db.create_all()

class UserModelTests(TestCase):

    def setUp(self):
        #clear database
        
        db.drop_all()
        db.create_all()

        #create user
        user_1 = User.signup('Tester1', 'test1@gmail.com', 'expassword111')
        user_1.id = 112

        db.session.commit()
    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    def test_user_model(self):

        u = User(
            username="User1",
            email="User@user.com",
            password="HASHED_PASSWORD"
        )
        #User should have no id before committing
        self.assertIsNone(u.id)

        db.session.add(u)
        db.session.commit()

        #User should have no Searches
        self.assertEqual(len(u.searches), 0)
        self.assertEqual(u.username,'User1')
        self.assertEqual(u.email,'User@user.com')
        self.assertEqual(u.password,'HASHED_PASSWORD')

    def test_valid_registration(self):

        u = User.signup(
            username="User1",
            email="User1@user.com",
            password="HASHED_PASSWORD2"
        )

        db.session.add(u)
        db.session.commit()
        #self.assertNotEqual(u.password, 'HASHED_PASSWORD2')
        self.assertIsNotNone(u.id)
        self.assertTrue(u.password.startswith('$2b$'))
        