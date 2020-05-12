from config.app_config import GEONAMES_USER, B64VAL
import requests
def retrieve_long_lat(arg):
    #Todo: URL for Canada and US http://api.geonames.org/postalCodeLookupJSON?postalcode=n4k5n8&country=CA&username=
    geonames = "http://api.geonames.org/searchJSON"
    resp_zip = requests.get(geonames, params={"q": arg, "username": GEONAMES_USER})
    geodata = resp_zip.json()
    lng = geodata['geonames'][0]['lng']
    lat = geodata['geonames'][0]['lat']
    
    return [lat, lng]

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
    watt_emissions = requests.get(watt_time_emission_url, params={"latitude": coords[0], "longitude": coords[1]}, headers=region_headers).json()
    print(watt_emissions)
    
    return watt_emissions