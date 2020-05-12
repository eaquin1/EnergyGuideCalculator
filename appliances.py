from app import db
from pathlib import Path
from openpyxl import load_workbook
import openpyxl.styles
from models import Appliance, User, UserSearch
import PyPDF2

db.drop_all()
db.create_all() 

#open xlsx file with appliances and wattage
xlsx_file = Path('static', '2.1.16.xlsx')

appliance_obj = openpyxl.load_workbook(xlsx_file)

wsheet = appliance_obj.active

## make list of appliance categories, from column A of 2.1.16.xlsx
# appliance_cats_cleaned = ['Kitchen', 'Lighting', 'Bedroom and Bathroom'...]

appliance_cats = [cell.value for cell in wsheet["A"] if cell.font.bold]
appliance_cats_cleaned = appliance_cats[3:]

## also extract the rows where the category titles are found, to get the correct rows for the appliances
# row_range = [(9, 14), (16, 19), (21, 22),...]
appliance_cats_rows = [cell.row for cell in wsheet["A"] if cell.font.bold][3:]
# append end range to rows
appliance_cats_rows.append(55)

row_range = []
for r in range(len(appliance_cats_rows)-1):
    ran = (appliance_cats_rows[r] + 1, appliance_cats_rows[r + 1] - 1)
    row_range.append(ran)


zipped = zip(appliance_cats_cleaned, row_range)
appliance_dict = dict(zipped) #{'Kitchen': (9, 14), 'Lighting': (16, 19, ...}


## make list of appliance instances to add to seed the database
appliances = []
for (cat, ra) in appliance_dict.items():
    for val in wsheet.iter_rows(min_row=ra[0], max_row =ra[1], values_only=True):
        appliance = Appliance(name=val[0],
                            watts=val[5],
                            category=cat)
        appliances.append(appliance)

# remove appliance from list if there is no wattage 
cleaned_appliances = [appl for appl in appliances if appl.watts != None]

## Supplement missing wattage information for washer, dryer, refrigerator, etc

pdfFileObj = open('static/1min_data.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

pageObj = pdfReader.getPage(0)
pageObj.extractText()

#Appliances wanted, wattage on line 14 of 1min_data.pdf
supplemental_appl = {
    'Washer (Normal Wash)': [66, 'Laundry Room'],
    'Dryer (Auto-regular)': [2873, 'Laundry Room'],
    'Wall AC': [24, 'Heating and Cooling'], 
    'Central AC': [2023, 'Heating and Cooling'], 
    'Range Oven': [2795, 'Kitchen'],
    'Dishwasher': [1172, 'Kitchen'],
    'Refrigerator': [366, 'Kitchen']
}

for name in supplemental_appl.keys():
    appliance = Appliance(name=name,
                            watts=supplemental_appl[name][0],
                            category=supplemental_appl[name][1])
    cleaned_appliances.append(appliance)


db.session.add_all([*cleaned_appliances])
db.session.commit()