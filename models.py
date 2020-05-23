"""SQLAlchemy models for Energy Guide"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Appliance(db.Model):
    """Appliances Wattage Model"""
    __tablename__ = "appliances"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    watts = db.Column(db.Integer)
    category = db.Column(db.Text)

    appliance_searches = db.relationship('UserSearch', backref='appliances', cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about appliance"""
        a = self
        return f"<Appliance {a.id} {a.name} {a.watts} {a.category}>"

class User(UserMixin, db.Model):
    """User Model"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    
    searches = db.relationship('UserSearch', backref='users', cascade="all, delete-orphan")
    
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
    daily_kWh = db.Column(db.Float, nullable=False)
    annual_Consump = db.Column(db.Float, nullable=False)
    annual_Cost = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    grid = db.Column(db.Text, nullable=False)
    gridpercent = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)

    @property
    def friendly_date(self):
        """"Return user friendly date"""
        return f'{self.timestamp.strftime("%b %d %Y %I:%M %p")}'

class Utility(db.Model):
    """Average utility rates by location"""
    __tablename__ = 'utilities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.Text, nullable=False)
    rate = db.Column(db.Float, nullable=False)




        