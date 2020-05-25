from config.app_config import GEONAMES_USER, B64VAL, PEXELS_API_KEY
from pexels_api import API
import requests

def retrieve_long_lat(zip):
    location_dict = {}

    if(len(zip) == 6 or len(zip) == 3 or len(zip)== 7):
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
    """Call the Pixabay API to return an image URL of the appliance. If there is no appropriate photo, use dictionary of URLs"""

    photo_dict = {
        "Wall AC": "https://i0.wp.com/homeairguides.com/wp-content/uploads/2020/02/best-through-the-wall-air-conditioners.jpg",
        "Central AC": "https://www.polspam.org/wp-content/uploads/2017/05/1.jpg",
        "Range Oven": "https://kitchenaid-h.assetsadobe.com/is/image/content/dam/business-unit/whirlpool/en-us/marketing-content/site-assets/page-content/ranges-sclp/ssb-removal/RangeSCLP_Masthead_Mobile_P180285_1z.jpg",
        "Waterbed Heater": "https://i5.walmartimages.com/asr/d6e84bf5-c480-4dde-b817-3bde1c7fa67b_1.e8fbe6f081dafe88251edf4a03a4f478.jpeg",
        "Televisions": "https://cnet3.cbsistatic.com/img/5AYR9m4W6Uu7GkTCa1TP9pN7AfQ=/868x488/2019/10/17/c272379f-4a92-4a77-9432-16f23703ea22/03-vizio-v-series-2019-v556-g1-v605-g3.jpg",
        'Analog, <40"': "https://cnet4.cbsistatic.com/img/99Yw213RfOcFayHaMojxDzlD_u0=/756x567/2012/02/28/861e600b-cc2e-11e2-9a4a-0291187b029a/old-polish-tv_1.jpg",
        'Analog, >40"': "https://cnet4.cbsistatic.com/img/99Yw213RfOcFayHaMojxDzlD_u0=/756x567/2012/02/28/861e600b-cc2e-11e2-9a4a-0291187b029a/old-polish-tv_1.jpg",
        'Digital, ED/HD TV, <40"':"https://scene7.samsclub.com/is/image/samsclub/0088727636930_A?wid=280&hei=280",
        'Digital, ED/HD TV, >40"': "https://scene7.samsclub.com/is/image/samsclub/0088727636930_A?wid=280&hei=280",
        'Set-top Boxes': "https://appliance-standards.org/sites/default/files/set-top_box.jpg",
        'DVD/VCR': 'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/4790/4790684_ra.jpg',
        'Dehumidifier': 'https://images.allergybuyersclub.com/img/TC-DE-PD7P-1-500.jpg',
        'Space Heater': 'https://images-na.ssl-images-amazon.com/images/I/71eohyKh2bL._AC_SX522_.jpg',
        'Water Heater-Family of 4': 'https://mobileimages.lowes.com/product/converted/035505/035505002440.jpg',
        'Portable Spa': 'https://www.diamondspas.com/wp-content/uploads/2018/07/MG_7601-Edit_Side_wood_bubbles_steps_72dpi_9X13.png',
        'Rechargeable Power Tool': 'https://i5.walmartimages.com/asr/2538ea03-9d15-4b68-89fa-c5f99f8f323a_1.8a29d0cf88517ba9881e157b2963fd6e.jpeg',
        'Well Pump': 'https://mpop-prod-hls-primary.s3.amazonaws.com/jones-services/img/1568475825-jones-services-1562082569Well-tank.jpg',
        'Aquarium Equipment': 'https://lh3.googleusercontent.com/proxy/xn0hkva7QPlevGbs6v-zrJnNJB1_Oi8RNkGCb2UwFTJV4U4ngjKVcbSdn79zKR-2x4rytMNp6wtq8nJe9x9NvwiwaQyTqiPw4Gqed1-LwQUQ9qRCkNkK8g',
        'Dryer (Auto-regular)': 'https://images.homedepot-static.com/productImages/ef33d316-3fa6-4e90-8d52-1fc65baee64c/svn/white-lg-electronics-electric-dryers-dle3500w-64_1000.jpg'
    }

    if photo_dict.get(appliance):
        image_url = photo_dict[appliance]
    else:
        api = API(PEXELS_API_KEY)
        try:
            search = api.search(appliance, results_per_page=1)
            image_url = search["photos"][0]["src"]["original"]
            
        except:
            image_url = "https://images.unsplash.com/photo-1519626504899-7a03a8a9ab51"
    return image_url
