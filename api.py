import json
import requests
def temp_tbilisi():
    key = '887aaff89bee4fd742287bfd4afa2483'
    city = 'Tbilisi'
    payload = {'q': city, 'appid': key, 'units': 'metric'}
    resp = requests.get('https://api.openweathermap.org/data/2.5/weather', params=payload)
    result = resp.json()
    x = result['main']['temp']
    return round(x)

def temp_kutaisi():
    key = '887aaff89bee4fd742287bfd4afa2483'
    city = 'Kutaisi'
    payload = {'q': city, 'appid': key, 'units': 'metric'}
    resp = requests.get('https://api.openweathermap.org/data/2.5/weather', params=payload)
    result = resp.json()
    y = result['main']['temp']
    return round(y)

def temp_batumi():
    key = '887aaff89bee4fd742287bfd4afa2483'
    city = 'Batumi'
    payload = {'q': city, 'appid': key, 'units': 'metric'}
    resp = requests.get('https://api.openweathermap.org/data/2.5/weather', params=payload)
    result = resp.json()
    y = result['main']['temp']
    return round(y)

