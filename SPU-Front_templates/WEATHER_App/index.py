from flask import Flask, session, redirect, url_for, escape, request, flash, render_template, Markup, make_response
import os, json, time, urllib2, urllib, datetime

app = Flask(__name__)

app.secret_key = 'dc367c6205529aa705c2afe6bd3222a3345a8243a50c291ee1635eaebccf353d'
api_key = '322552f7dea4bdc8e6da0c58faadabbb'

def get_weather(api_key, city, mode, units):
    form ={'q': city, 'mode':mode, 'units':units, 'APPID': api_key }
    data = urllib.urlencode(form)
    url = "http://api.openweathermap.org/data/2.5/forecast/daily/?" + data
    #print(url)
    response = urllib2.urlopen(url).read()
    return response

def laWeather():
    city = 'Los Angeles'
    weatherData = json.loads(get_weather(api_key, 'Los Angeles', 'json', 'standard'))
    city = weatherData.get("city")
    data = weatherData.get("list")
    return data, city

def weatherWeek(city):
    weatherData = json.loads(get_weather(api_key, city, 'json', 'standard'))
    data = weatherData.get("list")
    city = weatherData.get("city")
    for day in data:
        day['date'] = time.strftime('%m-%d-%Y', time.localtime(day['dt']))
    return data, city

@app.route('/index')
def index():
    return(render_template('index.html',))

@app.route("/")
#@app.route("/<searchcity>")
def default_route():
    searchcity = request.args.get("searchcity")
    remember = request.args.get("remember")
    if not searchcity:
        try:
            searchcity = request.cookies.get("last_city")
        except:
            pass
    if not searchcity:
        searchcity = 'London, UK'
    glob = get_weather2(api_key, searchcity, 'json', 'standard')
    data = json.loads(glob[0])
    forecast_list = glob[1]
    try:
        city = data['city']['name']
    except:
        return render_template('invalid_city.html', user_input=searchcity)
    country = data['city']['country']
    if not remember:
        response = make_response(render_template("weather2.html", forecast_list=forecast_list, city=city, country=country))
        return response
    response = make_response(render_template("weather2.html", forecast_list=forecast_list, city=city, country=country))
    response.set_cookie("last_city", "{},{}".format(city, country), expires=datetime.datetime.today() + datetime.timedelta(days=365))
    return response

@app.route("/laWeather")
def get_LA_weather():
    data = laWeather()[0]
    city = laWeather()[1]
    return render_template('city_weather.html', data=data, city=city )

@app.route("/weather/<city>")
@app.route("/weather/")
def get_city_weather(city='London'):
    if not request.args.get("searchcity"):
        glob = weatherWeek(city)
        data = glob[0]
        city = glob[1]
        return render_template('city_weather.html', data=data, city=city )
    searchcity = request.args.get("searchcity")
    glob = weatherWeek(searchcity)
    data = glob[0]
    city = glob[1]
    return render_template('city_weather.html', data=data, city=city )


@app.route('/invalid')
def invalid_entry():
    city = ''
    return render_template('invalid_city.html', city = city)

### Second Template

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
        description = (entry.get('weather')[0].get('description'))
        forecast_list.append( ( day, mini, maxi, description ) )
    return response, forecast_list

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    #import pdb; pdb.set_trace()
