from config.app_config import GEONAMES_USER, B64VAL
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
    # watt_emissions['city'] = coords['city']
    # watt_emissions['state'] = coords['state']
    
    return watt_emissions

# def util_rates():
#     """Use OpenEI API to populate utility rate based on area"""

#     openEI_base_url = "https://api.openei.org/utility_rates?version=3&format=json&"api_key=UTIL_API