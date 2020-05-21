
from flask import Flask, render_template, request, jsonify, Response, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Appliance, User, UserSearch, Utility
from os import environ
from forms import AddApplianceForm, NewUserForm, LoginUserForm
from flask_wtf.csrf import CSRFProtect
from API import login_watttime, retrieve_long_lat, retrieve_zipcode
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

@app.route("/", methods=["GET", "POST"])
def render_home():
    """Home page with calculator"""
    form = AddApplianceForm()
    #get appliances and utility rates from the database
    appliances = utils.get_categories()
    #utility_rates = utils.get_utility_rates()
    #populate select fields with database rates
    form.appliance.choices = appliances
    #form.rate.choices = utility_rates
    if session.get('search_key') == None:
        session['search_key'] = []

    if form.validate_on_submit():
        
        
        result = utils.calculate_consumption(form.watts.data, form.hours.data, form.days.data, form.rate.data)
        lat = session['location'][0]['lat']
        lng = session['location'][0]['lng']
        json_emissions = login_watttime(lat, lng)
        
        for key, value in json_emissions.items():
            result[key] = value
            
        result["appliance_id"] = form.appliance.data
        appliance_name = Appliance.query.get_or_404(result["appliance_id"])
        result["appliance_name"] = appliance_name.name
        result["city"] = session["location"][0]["city"]
        result["state"] = session["location"][0]["state"]
        
        #save to session
        search = session['search_key']
        search.append(result)
        session['search_key'] = search
        print(session)
        return render_template("results.html", result=result)
    
    return render_template('index.html', form=form)

@app.route("/watts/<int:id>")
def send_watts(id):
    """Return wattage of appliance"""
   
    if session['csrf_token']:
        appliance = Appliance.query.get_or_404(id)
        result = {"watts": appliance.watts}
       
        return jsonify(result)
    return redirect('/')
    

@app.route("/save", methods=["POST"])
def save_search():
    """Save a user search"""
    if current_user.is_authenticated:
        for search in session['search_key']:
            search_values = UserSearch(
                user_id = current_user.id,
                appliance_id = search['appliance_id'],
                daily_kWh = search['daily_kWh'],
                annual_Consump = search['annual_consump'],
                annual_Cost = search['annual_cost'],
                timestamp = search['point_time'],
                grid = search['ba'],
                gridpercent = search['percent'],
                state = search['state'],
                city = search['city']
            )
            db.session.add(search_values)
            db.session.commit()
        session.pop('search_key')
    return redirect("/")

@app.route("/delete-search/<int:id>", methods=["POST"])
@login_required
def delete_search(id):
    search = UserSearch.query.get_or_404(id)
    db.session.delete(search)
    db.session.commit()
    return redirect(f"/saved/{current_user.id}")

@app.route("/zipcode")
def look_up_zipcode():
    
    if request.args.get('zipcode'):
        zipc = request.args.get('zipcode')
        location_info = retrieve_long_lat(zipc)
    else:
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        location_info = retrieve_zipcode(lng, lat)
    
    utility = Utility.query.filter(Utility.location == location_info["state"]).first()
    location_info['rate'] = utility.rate
    #add lng, lat, city, state to session
    session['location'] = []
    location = session['location']
    location.append(location_info)
    session['location'] = location

    return jsonify(location_info)

# @app.route("/rates/<location>")
# def find_rate(location):
    
#     result = {"rate": state.rate}
#     return jsonify(result)

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

@app.route("/saved/<int:id>")
@login_required
def show_list(id):
    if current_user.is_authenticated:
        searches = UserSearch.query.filter_by(user_id=id)
        return render_template('searches.html', searches=searches)

    return redirect('/')

#     [('New England', ((21.63, 21.63), (21.63, 21.63))),
#  ('Connecticut', ((21.93, 21.93), (21.63, 21.63))),
#  ('Maine', ((16.79, 16.79), (21.63, 21.63))),
#  ('Massachusetts', ((22.91, 22.91), (21.63, 21.63))),
#  ('New Hampshire', ((20.23, 20.23), (21.63, 21.63))),
#  ('Rhode Island', ((24.24, 24.24), (21.63, 21.63))),
#  ('Vermont', ((19.27, 19.27), (21.63, 21.63))),
#  ('Middle Atlantic', ((15.41, 15.41), (21.63, 21.63))),
#  ('New Jersey', ((15.43, 15.43), (21.63, 21.63))),
#  ('New York', ((17.55, 17.55), (21.63, 21.63))),
#  ('Pennsylvania', ((13.63, 13.63), (21.63, 21.63)))]
