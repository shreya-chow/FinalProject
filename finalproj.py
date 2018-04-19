import json
import requests
import sqlite3 as sqlite
import secretsproj
import time
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
plotly.tools.set_credentials_file(username= secretsproj.plotlyuser, api_key= secretsproj.plotlyapi)

conn = sqlite.connect('restaurant.db')
cur = conn.cursor()


CACHE_FNAME = 'finalproj.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

def make_request_using_cache(baseurl, params, headers = {}):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]

    else:
        resp = requests.get(baseurl, params, headers= headers)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

class Restaurant():
    def __init__(self, datadict):
        self.name = datadict["name"]
        self.rating = datadict["rating"]
        self.distance = datadict["distance"]
        self.category = datadict["categories"][0]["title"]
        try:
            self.price = len(datadict['price'])
        except:
            self.price = None
        self.address1 = " ".join(datadict["location"]["display_address"])

    def __str__(self):
        return "{} with rating {} stars and price {}.".format(self.name, self.rating, "$"*self.price)

def getyelpdata(googleid):
    statement = "SELECT lat,lng FROM Google WHERE Id = ?"
    cur.execute(statement, (googleid,))
    lat,lng = cur.fetchone()
    baseurl = "https://api.yelp.com/v3/businesses/search"
    location = make_request_using_cache(baseurl, params = {"latitude": lat, "longitude":lng, "limit": 50}, headers = {"Authorization": "Bearer {}".format(secretsproj.apisecret)})["businesses"]
    location2 = make_request_using_cache(baseurl, params = {"latitude": lat, "longitude":lng, "limit": 50, "offset": 50}, headers = {"Authorization": "Bearer {}".format(secretsproj.apisecret)})["businesses"]
    all_locs = location + location2
    Restaurants = [Restaurant(dict) for dict in all_locs]
    for place in Restaurants:
         statement = "INSERT INTO 'Yelp' VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
         cur.execute(statement, (place.name, place.rating, place.distance, place.category, place.address1, None, googleid, place.price))
    return all_locs


def getgoogledata(location_str):
    baseurl2 = "https://maps.googleapis.com/maps/api/geocode/json"
    googlelocations = []
    location = make_request_using_cache(baseurl2, params = {"address": location_str, "key": secretsproj.apigoogle})
    zipcode = location["results"][0]["address_components"][0]["long_name"]
    state = location["results"][0]["address_components"][4]["long_name"]
    formatted_address = location["results"][0]["formatted_address"]
    lat = location["results"][0]["geometry"]["location"]["lat"]
    lng = location["results"][0]["geometry"]["location"]["lng"]
    statement = "INSERT INTO 'Google' VALUES (?, ?, ?, ?, ?, ?)"
    cur.execute(statement, (zipcode, state, formatted_address, lat, lng, None))
    statement1 = "SELECT Id FROM Google WHERE zipcode = ?"
    cur.execute(statement1, (location_str.strip(),))
    return cur.fetchone()[0]

def table():
    cur.execute("DROP TABLE if exists 'Google'")
    cur.execute("DROP TABLE if exists 'Yelp'")
    statement = "CREATE TABLE if NOT EXISTS 'Google' ('zipcode' text, 'state' text, 'formatted_address' text, 'lat' real, 'lng' real, 'id' INTEGER PRIMARY KEY AUTOINCREMENT)"
    cur.execute(statement)
    statement = "CREATE TABLE if NOT EXISTS 'Yelp' ('name' text, 'rating' real, 'distance' real, 'category' text, 'address1' text, 'id' INTEGER PRIMARY KEY AUTOINCREMENT, 'googleid' integer, 'price' integer)"
    cur.execute(statement)

conn.commit()

def getdistance(googleid, showViz = True):
    statement = "SELECT distance FROM Yelp WHERE googleid = ? AND rating > 4 ORDER BY distance asc"
    cur.execute(statement, (googleid,))
    distancelist = [t[0] for t in cur.fetchall()]

    trace = go.Scatter(
    x = list(range(len(distancelist))),
    y = distancelist,
    mode = 'markers'
    )

    data = [trace]
    layout = dict(title = 'Distance(m) of Restaurants over 4 Stars near your location', xaxis=dict(title='count'),yaxis=dict(title='distance(m)',))

    fig = dict(data=data, layout=layout)
    if showViz:
        py.plot(fig, filename= 'distance')
    return distancelist

def getprice(googleid, showViz = True):
    statement = "SELECT price FROM Yelp WHERE googleid = ? AND rating > 3 ORDER BY price asc"
    cur.execute(statement, (googleid,))
    pricelist = [t[0] for t in cur.fetchall() if t[0] != None]

    trace = go.Scatter(
    x = list(range(len(pricelist))),
    y = pricelist,
    mode = 'markers'
    )

    data = [trace]
    layout = dict(title = 'price of Restaurants over 3 Stars near your location', xaxis=dict(title='count'),yaxis=dict(title='price',))

    fig = dict(data=data, layout=layout)
    if showViz:
        py.plot(fig, filename= 'price')
    return pricelist


def category(googleid, showViz = True):
    statement = "SELECT category FROM Yelp WHERE googleid = ? AND rating >= 3"
    cur.execute(statement, (googleid,))
    pricelist = [t[0] for t in cur.fetchall()]
    dictcount = {Cuisine: pricelist.count(Cuisine) for Cuisine in pricelist}
    labels = list(dictcount.keys())
    values = list(dictcount.values())

    trace = go.Pie(labels=labels, values=values)

    layout = go.Layout(title= 'Distribution of Cuisines over 3 stars near your location')
    fig = go.Figure(data=[trace], layout= layout)
    if showViz:
        py.plot(fig, filename= 'basic_pie_chart')
    return dictcount

def groupedbar(googleid, showViz = True):
    statement = "SELECT rating FROM Yelp WHERE googleid = ? AND price >1 and price <= 2"
    cur.execute(statement, (googleid,))
    ratinglist = [t[0] for t in cur.fetchall()]
    dictcount = {rating: ratinglist.count(rating) for rating in ratinglist}
    x = list(dictcount.keys())
    y = list(dictcount.values())

    trace1 = go.Bar(
        x=x,
        y=y,
        name='> $ and <= $$'
    )

    statement = "SELECT rating FROM Yelp WHERE googleid = ? AND price >2 and price <= 3"
    cur.execute(statement, (googleid,))
    ratinglist = [t[0] for t in cur.fetchall()]
    dictcount = {rating: ratinglist.count(rating) for rating in ratinglist}
    x1 = list(dictcount.keys())
    y1 = list(dictcount.values())

    trace2 = go.Bar(
        x=x1,
        y=y1,
        name='> $$ and <= $$$'
    )

    statement = "SELECT rating FROM Yelp WHERE googleid = ? AND price >3 and price <= 4"
    cur.execute(statement, (googleid,))
    ratinglist = [t[0] for t in cur.fetchall()]
    dictcount = {rating: ratinglist.count(rating) for rating in ratinglist}
    x2 = list(dictcount.keys())
    y2 = list(dictcount.values())

    trace3 = go.Bar(
        x=x2,
        y=y2,
        name='> $$$ and <= $$$$'
    )

    statement = "SELECT rating FROM Yelp WHERE googleid = ? AND price >4 and price <= 5"
    cur.execute(statement, (googleid,))
    ratinglist = [t[0] for t in cur.fetchall()]
    dictcount = {rating: ratinglist.count(rating) for rating in ratinglist}
    x3 = list(dictcount.keys())
    y3 = list(dictcount.values())

    trace4 = go.Bar(
        x=x3,
        y=y3,
        name='> $$$$ and <= $$$$$'
    )


    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    if showViz:
        py.plot(fig, filename='grouped-bar')

    return [x, y, x1, y1, x2, y2, x3, y3]





if __name__ == "__main__":
    table()
    user_input = None
    googleid = None
    while True:
        if user_input:
            user_input = input("""Type a US zip code or choose a visualization 1, 2, 3 or 4
            1. = This visualization shows you a scatterplot of distance in meters of Restaurants over 4 Stars near your entered zip code.
            2. = This visualization shows you a scatterplot of price ($ to $$$$) of Restaurants over 3 Stars near your entered zip code.
            3. = This visualization shows you a pie graph of the distribution of cuisines over 3 stars near your entered zip code.
            4. = This visualization shows you a grouped bar graph of price distruibutions restaurants of each rating near your entered zip code
            """)
            if user_input == "1":
                getdistance(googleid)
            elif user_input == "2":
                getprice(googleid)
            elif user_input == "3":
                category(googleid)
            elif user_input == "4":
                groupedbar(googleid)
            elif len(user_input) == 5 and user_input.isnumeric():
                googleid = (getgoogledata(user_input))
                getyelpdata(googleid)
                conn.commit()
            else:
                print("Enter a valid command.")
                continue
        else:
            user_input = input("Type a US zip code ")
            if len(user_input) != 5 or not user_input.isnumeric():
                print("Error, type a valid US zip code")
                user_input = None
                continue
            googleid = (getgoogledata(user_input))
            getyelpdata(googleid)
            conn.commit()








        #getdistance(googleid)
        #getprice(googleid)
        # category(googleid)
        # groupedbar(googleid)












#for x in (location["results"]):


#name, rating, formatted_address
