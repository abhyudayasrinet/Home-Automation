import forecastio
import requests
import json

API_KEY = "f5af7c9d5dcae926c4e5fcf75ea35dc6"

send_url = "http://ip-api.com/json"

r = requests.get(send_url)
j = json.loads(r.text)

latitude = j['lat']
longitude = j['lon']
print("current latitude, longitude is ", latitude, longitude)

forecast = forecastio.load_forecast(API_KEY, latitude, longitude)
#print(forecast)
#j = json.loads(forecast.text)
datapoint = forecast.currently()
print(datapoint.summary)
print(datapoint.temperature)
print(datapoint.precipProbability)
