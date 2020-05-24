"""User model tests"""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///energy-test"

from app import app

db.create_all()

class UserModelTests(TestCase):

    def setUp(self):
        #clear database
        db.session.close()
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    #####
    #
    # Signup Tests
    #
    #####

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
        self.assertNotEqual(u.password, 'HASHED_PASSWORD2')
        self.assertIsNotNone(u.id)
        self.assertTrue(u.password.startswith('$2b$'))

    def test_invalid_username_signup(self):
        invalid = User.signup(None, "test@test.com", "pass")
        invalid.id = 1234

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError):
            User.signup("testertester", "email@email.com", "")

        with self.assertRaises(ValueError):
            User.signup("test344", "e344@email.com", None)

     #####
    #
    # Authentication Tests
    #
    #####

    def test_valid_authenication(self):
        user_1 = User.signup('Mememe', 'email@here.com', 'passiepassie')
        user = User.authenticate(user_1.username, "passiepassie")
        self.assertIsNotNone(user)
        self.assertEqual(user.id, user_1.id)

    def test_invalid_password_authentication(self):
        user_1 = User.signup('Tester1', 'test1@gmail.com', 'expassword111')
        self.assertFalse(User.authenticate(user_1.username, "What do I put here?"))

    def test_invalid_username_authentication(self):
        self.assertFalse(User.authenticate("someone", "password"))
        