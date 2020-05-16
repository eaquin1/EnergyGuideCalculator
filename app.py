
from flask import Flask, render_template, request, jsonify, Response, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Appliance, User, UserSearch
import requests
from os import environ
from forms import AddApplianceForm, NewUserForm, LoginUserForm
from flask_wtf.csrf import CSRFProtect
from API import login_watttime, retrieve_long_lat
import utils
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

app = Flask(__name__)
csrf = CSRFProtect(app)

# use local development config vars if folder exists, otherwise use environment vars
# '/config' folder should never be tracked in source control!
import importlib
dev_config = importlib.util.find_spec('config')
if dev_config is not None:
    from config.app_config import DB_URI, SECRET_KEY
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
else:
    DB_URI = environ.get('DATABASE_URL')
    SECRET_KEY = environ.get('SECRET_KEY')

app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/", methods=["GET"])
def render_home():
    """Home page with calculator"""
    form = AddApplianceForm()
    appliances = utils.get_categories()
    
    form.appliance.choices = appliances
    
    return render_template('index.html', form=form)

@app.route("/watts/<int:id>")
def send_watts(id):
    """Return wattage of appliance"""
   
    if session['csrf_token']:
        appliance = Appliance.query.get_or_404(id)
        result = {"watts": appliance.watts}
       
        return jsonify(result)
    return redirect('/')
    

@app.route("/calculate")
def calculate():
    """Calculate electricity costs with user input
    Returns JSON:{'watts': 2023.0, 'rate': 0.12, 'hours': 4.0, 'days': 25.0, 'freq': '300', 'ba': 'ERCOT_NORTH', 'percent': '55', 'point_time': '2020-05-16T22:55:00Z', 'city': 'Denton', 'state': 'Texas'} """
    if session['csrf_token']:
        calc_dict = {}
        #calculate electricity usage
        for arg in request.args:
            if request.args.get(arg):
                calc_dict[arg] = float(request.args.get(arg))
        
        result = utils.calculate_consumption(calc_dict)
        print("calc", result)

        # calculate cleanliness values and location values
        zipcode = request.args.get('zipcode')
        coords = retrieve_long_lat(zipcode)
        json_emissions = login_watttime(coords)

        #add the results to the result dictionary
        for key, value in json_emissions.items():
            result[key] = value
        
        result["appliance_id"] = request.args.get('applianceId')
        #if current_user.is_authenticated:
        if session.get('search_key') == None:
            session['search_key'] = []
        else:
            search = session['search_key']
            search.append(result)
            session['search_key'] = search
        print(session['search_key'])
        return jsonify(result)
    return redirect('/')


# @app.route("/save", methods=["POST"])
# def save_search():


## USER ROUTES ##

@app.route("/logout")
def logout():
    logout_user()
    flash('Successfully logged out', 'info')
    return redirect('/')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup
    Create new user and add to DB"""
    form = NewUserForm()
    
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data
            )
            db.session.commit()
            flash(f"Welcome to EnergyGuide, {user.username}", "secondary")
        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template('signup.html', form=form)
        login_user(user)
        return redirect("/")
    else:
        return render_template('signup.html', form=form)    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginUserForm()
    
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user is False:
            flash('Invalid login credentials. Please try again', 'danger')     
            return redirect("/login")
        else:
            login_user(user, remember=form.remember.data)
            flash(f"Hello, {user.username}!", "success")
            return redirect('/')

    return render_template('login.html', form=form)

    