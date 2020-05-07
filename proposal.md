# Electricity Power Consumption Calculator

The target users for this website are people who would like to be aware of their electricity usage, both for saving money in utility bills, and to help reduce carbon emissions.

## Background

While there have been great strides in green energy production, such as wind and solar power, the consumption needs of the grid do not always align with the availability of renewable energy. The startup Watt Time has software called Automated Emissions Reduction that allows smart appliances to decrease electricity consumption during peak grid usage, and increase consumption when it is less taxing on the grid. However, it will be a while before this technology is widespread, while a user may still want information on their consumption so they can tailor their power usage manually. This calculator aims to empower users to make more informed decisions on their electricity usage.

## Calculator
I would like to build an interactive "EnergyGuide" calculator, similar to the yellow sticker found on appliances when you purchase them.
The website will allow a user to pick an appliance. The calculator will suggest a wattage, based on data I have from an API (or web scraped), but it can be adjusted up or down, since the user's appliance may be slightly different than the norm. I will suggest an average utility rate (maybe $0.12kWh), which can also be adjusted by the user. Finally, the user will estimate the number of hours it's used per day, and the number of days used per year. The calculator will return the energy use (kWh) and cost for the year.

## Current Grid Usage
I will also use the [Watt Time API](https://watttime.org) to allow the user to input their zipcode or postal code. I will use [GeoNames API](https://www.geonames.org/maps/addresses.html#geoCodeAddress) to convert the zipcode to long/lat, which is used by the Watt Time API. Watt Time will return a number between 0 to 100. The higher the number, the dirtier the grid is running at the time the user enters their zipcode. If the number is high, the user can consider waiting until a non-peak time to use their appliance.

I would also like to let a user create an account. When they are logged in, they can access previous search results.
