import requests
from pprint import pprint
city = 'Sochi'
my_params = {
    'q': city,
    'appid': ''
}

url = 'http://api.openweathermap.org/data/2.5/weather'

response = requests.get(url, params=my_params)
json_data = response.json()

pprint(
    f'В городе {json_data.get("name")} температура {json_data.get("main").get("temp") - 273.15} градусов')
