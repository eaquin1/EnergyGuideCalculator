from config.app_config import GEONAMES_USER, B64VAL, PIXABAY_KEY
import requests
def retrieve_long_lat(zip):
    location_dict = {}

    if(len(zip) == 6 or len(zip) == 3):
        country = 'CA'
    elif(len(zip) == 5):
        country = 'US'

    geonames = "http://api.geonames.org/postalCodeLookupJSON"
    resp_coords = requests.get(geonames, params={"postalcode": zip, "country": country, "username": GEONAMES_USER})
    geodata = resp_coords.json()
    location_dict['lng'] = geodata['postalcodes'][0]['lng']
    location_dict['lat'] = geodata['postalcodes'][0]['lat']
    location_dict['city'] = geodata['postalcodes'][0]['placeName']
    location_dict['state'] = geodata['postalcodes'][0]['adminName1']
    location_dict['zip'] = zip

    return location_dict

def retrieve_zipcode(lng, lat):
    zip_dict = {}
    geonames = "http://api.geonames.org/findNearbyPostalCodesJSON?"
    resp = requests.get(geonames, params={"lat": lat, "lng": lng, "username": GEONAMES_USER})
    geodata = resp.json()
    zip_dict["zip"] = geodata['postalCodes'][0]['postalCode']
    zip_dict["state"] = geodata['postalCodes'][0]['adminName1']
    zip_dict["city"] = geodata['postalCodes'][0]['placeName']
    zip_dict["lng"] = lng
    zip_dict["lat"] = lat
    
    return zip_dict

def login_watttime(lat, lng):
    """Call the Watt Time API to receive grid cleanliness data. 
    Params: lat and lng
    Returns: {'freq': '300', 'ba': 'ERCOT_NORTH', 'percent': 48, 'point_time': '2020-05-21T22:15:00Z'} """
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
    
    #turn percent into an integer
    watt_emissions["percent"] = int(watt_emissions["percent"])
    return watt_emissions

def get_photo(appliance):
    """Call the Pixabay API to return an image URL of the appliance"""
    pixa_base_url = "https://pixabay.com/api/"
    try:
        pixabay = requests.get(pixa_base_url, params={"key": PIXABAY_KEY, "q": appliance, "safesearch": True})
        pixabay_resp = pixabay.json()
        image_url = pixabay_resp["hits"][0]["webformatURL"]
        print(image_url)
    except:
        image_url = "https://images.unsplash.com/photo-1519626504899-7a03a8a9ab51"
    return image_url