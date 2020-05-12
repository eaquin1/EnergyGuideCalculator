"""SQLAlchemy models for Energy Guide"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Appliance(db.Model):
    """Appliances Wattage Model"""
    __tablename__ = "appliances"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    watts = db.Column(db.Integer)
    category = db.Column(db.Text)

    appliance_searches = db.relationship('UserSearch', backref='appliances')

    def __repr__(self):
        """Show info about appliance"""
        a = self
        return f"<Appliance {a.id} {a.name} {a.watts} {a.category}>"

class User(db.Model):
    """User Model"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    
    searches = db.relationship('UserSearch', backref='users')
    
    def __repr__(self):
        u = self
        return f"<User #{u.id}: {u.username}, {u.email}>"
    
    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.
        Hashes password and adds user to system.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Search for a user and return the user object. 
        If the user cannot be found, return False"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False

class UserSearch(db.Model):
    """Searches from a user model"""
    __tablename__ = 'user_searches'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    appliance_id = db.Column(db.Integer, db.ForeignKey('appliances.id', ondelete='CASCADE'), nullable=False)
    watts = db.Column(db.Float, nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    grid = db.Column(db.Text, nullable=False)
    gridpercent = db.Column(db.Integer, nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)





        