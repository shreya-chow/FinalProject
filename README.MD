The data sources I used are
- Google Geocoding API (https://developers.google.com/maps/documentation/geocoding/start)
- Yelp Fusion API (https://www.yelp.com/fusion)

Create a file called secretsproj.py
set these values:
apisecret = "" #yelp api key goes here
https://www.yelp.com/developers/v3/manage_app
apigoogle = "" #google api key goes here
https://developers.google.com/maps/documentation/geocoding/start #click get a key in the right corner of the page
plotlyuser = "" #plotly usernmame goes here
https://plot.ly/settings/api
plotlyapi = "" #plotly api key goes here
https://plot.ly/settings/api

#write these lines on your code file to connect your secrets file to your code file
import secretsproj
import plotly
plotly.tools.set_credentials_file(username= secretsproj.plotlyuser, api_key= secretsproj.plotlyapi)



I set up the cache in the beginning. The class defines all the variables that I am getting like the address, name, distance, rating, and price. Since not all variables on Yelp have a price. I made a try/except so my program runs. I also have a getyelpdata function that gets all the yelp data for the restaurants near an entered zip code. I have getgoogledata function that gets all the google data for the restaurants near an entered zip code.

The user types in zip code and if zip code is valid then they are prompted to enter another zip code or choose a visualization.
They choose from 4 different presentations that represent different distributions of price and rating and distance in the area. They press either 1 or 2 or 3 or 4 to choose a visualization. 
