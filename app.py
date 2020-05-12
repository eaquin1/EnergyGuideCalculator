
from flask import Flask, render_template, request, jsonify, Response, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Appliance
import requests
from os import environ
from forms import AddApplianceForm
from flask_wtf.csrf import CSRFProtect
from config.app_config import GEONAMES_USER, B64VAL
import utils

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
        print(calc_dict)
        result = utils.calculate_consumption(calc_dict)
    
        return jsonify(result)
    return redirect('/')

@app.route("/grid")
def return_grid_value():
    """Return grid cleanliness value. First call GeoNames API to get longitude and latitude, then call Watt Time API"""
    if session['csrf_token']:
        
        zipcode = request.args.get('zipcode')
        #Todo: URL for Canada and US http://api.geonames.org/postalCodeLookupJSON?postalcode=n4k5n8&country=CA&username=
        geonames = "http://api.geonames.org/searchJSON"
        resp_zip = requests.get(geonames, params={"q": zipcode, "username": GEONAMES_USER})
        geodata = resp_zip.json()
        lng = geodata['geonames'][0]['lng']
        lat = geodata['geonames'][0]['lat']
        
        #Watt time API calls
        wt_base_url = "https://api2.watttime.org/v2"
        headers = {
                'Authorization': 'Basic %s' % B64VAL
                }
        #login to WattTime to get token
        watt_time_login_url = f"{wt_base_url}/login/"
        watt_time_token = requests.get(watt_time_login_url, headers = headers).json()
        
        region_headers = {
            'Authorization': 'Bearer %s' % watt_time_token['token']
        }
        
        #get real time emissions for region
        watt_time_emission_url = f"{wt_base_url}/index"
        watt_emissions = requests.get(watt_time_emission_url, params={"latitude": lat, "longitude": lng}, headers=region_headers).json()
        
        return watt_emissions
    return redirect('/')