import requests
from bs4 import BeautifulSoup

data = requests.get('http://web.archive.org/web/20130216233647/http://buildingsdatabook.eren.doe.gov/TableView.aspx?table=2.1.16')
soup = BeautifulSoup(data.text, "html.parser")