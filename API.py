from config.app_config import GEONAMES_USER, B64VAL
import requests
def retrieve_long_lat(arg):
    location_dict = {}

    if(len(arg) == 6):
        country = 'CA'
    elif(len(arg) == 5):
        country = 'US'
    geonames = "http://api.geonames.org/postalCodeLookupJSON"
    resp_zip = requests.get(geonames, params={"postalcode": arg, "country": country, "username": GEONAMES_USER})
    geodata = resp_zip.json()
    location_dict['lng'] = geodata['postalcodes'][0]['lng']
    location_dict['lat'] = geodata['postalcodes'][0]['lat']
    location_dict['city'] = geodata['postalcodes'][0]['placeName']
    location_dict['state'] = geodata['postalcodes'][0]['adminName1']

    return location_dict

def login_watttime(coords):
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
    watt_emissions = requests.get(watt_time_emission_url, params={"latitude": coords['lat'], "longitude": coords['lng']}, headers=region_headers).json()
    watt_emissions['city'] = coords['city']
    watt_emissions['state'] = coords['state']
    print(watt_emissions)
    
    return watt_emissions