# EnergyGuide

**EnergyGuide is an interactive calculator to enable the user to make informed decisions on their electricity usage**

EnergyGuide is intended to give you more information to tailor your energy usage to your budget and to the needs of your local electricity grid. While there are more sources of clean energy than ever before, the energy isn't always produced when the grid load is highest. For example, wind turbines might harvest large amounts of energy in the middle of the night, but the grid needs the energy during the day, when air conditioners are used to combat the afternoon heat. The technology for storing wind and solar energy is lagging behind the electricity needs of the grid.

This is where [Watt Time](https://www.watttime.org/) comes in. They created Automated Emissions Reduction (AER) technology to enable smart devices to run when the grid is cleanest. However, not everyone is using smart devices (yet). Watt Time collects data every 5 minutes to compare the cleanliness of each grid in the United States and Canada, and reports how dirty the grid is running, in a percentage.

EnergyGuide will report the current grid data for your location, and it also combines information on the energy usage for various appliances. The inspiration is the yellow sticker you'll find on various appliances when you buy them. You can input your appliance, and edit the wattage of your particular appliance, while also entering your price of electricity. EnergyGuide will tell you how much electricity your item uses on a daily basis, yearly basis, and how much that costs you. If you create an account, you can save your searches and track the cleanliness of your grid during various points during the day.

The appliance and utility data was web scraped from the 2010 Buildings Energy Databook, Table 2.1.16; the EIA Electric Power Monthly, Table 5.06;, and [EnergyHub](https://www.energyhub.org/electricity-prices/)

## Demo
**Live demo deployed to https://energy-guide.herokuapp.com**

![alt demo](https://github.com/eaquin1/EnergyGuideCalculator/blob/master/static/eguide.gif?raw=true)

## Installation

On your local machine, you will need to create a Postgres database, set up a virtual environment in Pyhton, and create API credentials for [Watt Time](https://www.watttime.org/), [GeoNames](https://www.geonames.org) and [Pexels](https://www.pexels.com).

```
> git clone https://github.com/eaquin1/EnergyGuideCalculator.git
> python -m venv venv
> pip install -r requirements.txt
> source venv/bin/activate
```

## Authors

- Emily Aquin - [Github](https://github.com/eaquin1) - [Website](https://sharpdesigns.xyz)
