
from flask import Flask, render_template, request, jsonify, Response
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Appliance
from os import environ
from forms import AddApplianceForm
from flask_wtf.csrf import CSRFProtect
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
    
    appliances = utils.get_categories()

    return render_template('index.html', appl = appliances)

@app.route("/watts/<int:id>")
def send_watts(id):
    """Return wattage of appliance"""

    appliance = Appliance.query.get_or_404(id)
    result = {"wattage": appliance.watts}
    return jsonify(result)

@app.route("/calculate")
def calculate():
    calc_dict = {
        "watts": 0,
        "rate": 0,
        "hours": 0,
        "days": 0
    }
    print(request.form.get('wattage'))
    if request.form.get('wattage'):
        calc_dict["watts"] = request.form.get('wattage')
    
    if request.form.get('rate'):
        calc_dict["rate"] = request.form.get('rate')
    
    if request.form.get('hours'):
        calc_dict['hours'] = request.form.get('hours')
    
    if request.form.get('days'):
        calc_dict['days'] = request.args.get('days')
    print(calc_dict)
    result = utils.calculate_consumption(calc_dict)
    print(result)
    return jsonify(result)