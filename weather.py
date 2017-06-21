import json
import requests
import variables


WEATHER_API = 'http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid={1}'
city_name = 'Kiev'


class Weather:
    def __init__(self, city_name, key):
        self.city_name = city_name
        self.key = key
        self.response = json.loads(requests.get(WEATHER_API.format(
            self.city_name,
            self.key)).text
        )

    def get_weather(self):
        humidity = str(self.response['main']['humidity'])
        temperature = str(self.response['main']['temp'])
        wind = str(self.response['wind']['speed'])
        return temperature, humidity, wind

    def get_coordinates(self):
        latitude = str(self.response['coord']['lat'])
        longitude = str(self.response['coord']['lon'])
        return latitude, longitude
