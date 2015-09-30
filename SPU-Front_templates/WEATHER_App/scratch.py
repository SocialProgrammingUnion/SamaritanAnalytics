### Starting Point
def index():
    data = json.loads(get_weather(api_key, 'Los Angeles', 'json', 'standard'))
    page = "<html><head><title>My Weather</title></head><body>"
    page += "<h1>Weather for {}, {}</h1>".format(data.get('city').get('name'), data.get('city').get('country'))
    for day in data.get("list"):
        page += "<b>date:</b> {} <b>min:</b> {} <b>max:</b> {} <b>description:</b> {} <br/>".format(
        time.strftime('%d %B', time.localtime(day.get('dt'))),
        (day.get("temp").get("min")),
        day.get("temp").get("max"),
        day.get("weather")[0].get("descripton"))
    page += "</body></html>"
    return page

### Table Template

@app.route("/weather2/<city>")
def get_city_weather2(city):
    glob = get_weather2(api_key, city, 'json', 'standard')
    data = glob[0]
    forecast_list = glob[1]
    return render_template('weather2.html', data=data, forecast_list=forecast_list )

def get_weather2(api_key, city, mode, units):
    form ={'q': city, 'mode':mode, 'units':units, 'APPID': api_key }
    data = urllib.urlencode(form)
    url = "http://api.openweathermap.org/data/2.5/forecast/daily/?" + data
    #print(url)
    response = urllib2.urlopen(url).read()
    data = json.loads(response)
    forecast_list = []
    for entry in data.get("list"):
        day = time.strftime('%d, %B', time.localtime(entry.get('dt')))
        mini = (entry.get("temp").get("min"))
        maxi = (entry.get("temp").get("max"))
        description = (entry.get('description'))
        forecast_list.append((day,mini,maxi,description))
    return response, forecast_list

### Hello Word Stuff

@app.route("/hello")
def hello():
    flash( Markup("Hello <strong>Weather World!</strong>"))
    return render_template('index.html');

@app.route("/hello/<name>")
def hello_name(name):
    flash( Markup("<strong>Hello, Access from %s</strong>" % name))
    return render_template('index.html');

@app.route("/hello/<name>/<int:age>")
def hello_name_age(name, age):
    flash( Markup("<strong>Hello, Access from %s</strong>" % name))
    flash( Markup("<strong>%s is %s Years old" % (name,age)))
    return render_template('index.html')

@app.route("/goodbye")
def goodbye():
    flash( Markup("Goodbye <strong>Weather World!</strong>"))
    return render_template('goodbye.html')
