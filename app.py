
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

@app.route("/", methods=["GET", "POST"])
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
    Returns JSON:{'watts': 2023.0, 'rate': 0.12, 'hours': 4.0, 'days': 25.0} """
    if session['csrf_token']:
        calc_dict = {}
        
        for arg in request.args:
            if request.args.get(arg):
                calc_dict[arg] = float(request.args.get(arg))
        
        result = utils.calculate_consumption(calc_dict)
    
        return jsonify(result)
    return redirect('/')

@app.route("/grid")
def return_grid_value():
    """Return grid cleanliness value. First call GeoNames API to get longitude and latitude, then call Watt Time API"""
    if session['csrf_token']:
        zipcode = request.args.get('zipcode')
        coords = retrieve_long_lat(zipcode)
        json_emissions = login_watttime(coords)
        return json_emissions
    
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
        return redirect("/")
    else:
        return render_template('signup.html', form=form)    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginUserForm()
    print(form.validate())
    if form.validate_on_submit():
        print("hello?")
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)