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

user types in zip code and if zip code is valid then they are prompted to enter another zip code or choose a visualization.
They choose from 4 different presentations that represent different distributions of price and rating and distance in the area.


The class definition

getyelpdata gets data from yelp

getgoogledata




Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.
Brief user guide, including how to run the program and how to choose presentation options.
