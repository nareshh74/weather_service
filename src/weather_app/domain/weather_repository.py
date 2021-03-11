import json
import os
import requests
from openpyxl import Workbook
import traceback
from django.conf import settings


class WeatherRepository(object):

    def __init__(self):
        # self.cities_list = ["Hong Kong", "Bangkok", "London", "Macau", "Singapore", "Paris", "Dubai", "New York", "Kuala Lumpur", "Istanbul", "Delhi", "Antalya", "Shenzhen",
        #                     "Mumbai", "Phuket", "Rome", "Tokyo", "Pattaya", "Taipei", "Mecca", "Guangzhou", "Prague", "Medina", "Seoul", "Amsterdam", "Agra", "Miami", "Osaka", "Las Vegas", "Shanghai"]
        self.cities_list = ["Hong Kong", "Bangkok", ]
        self.weather_data = {}
        self.json_file = os.path.join(settings.STATIC_FILES_PATH, "weather_data.json")
        self.excel_file = os.path.join(settings.STATIC_FILES_PATH, "weather_data.xlsx")
        self.openweather_api_key = settings.OPENWEATHER_API_KEY
        self.openweather_api_endpoint = settings.OPENWEATHER_API_ENDPOINT

    def query(self, start_index, end_index):
        result = {}
        # if not self.weather_data:
        json_file = open(self.json_file, "r")
        print(json_file.name)
        self.weather_data = json.load(json_file)
        for city in self.cities_list[start_index: end_index + 1]:
            result[city] = self.weather_data[city]
        return result

    def get_data_as_excel(self):
        return self.excel_file

    def get_city_count(self):
        return len(self.cities_list)

    def sync(self):
        print("sync start")
        try:
            self.weather_data = {}
            for city in self.cities_list:
                response = requests.get(self.openweather_api_endpoint,
                                        params={"q": city, "appid": self.openweather_api_key}).text
                data = json.loads(response)
                self.weather_data[city] = {"description": data["weather"][0]["description"],
                                           "temperature": data["main"]["temp"],
                                           "pressure": data["main"]["pressure"],
                                           "humidity": data["main"]["humidity"]}
            self._persist(self.weather_data)
        except Exception as e:
            traceback.print_exc()
            raise Exception("sync failed")
        print("sync end")

    def _persist(self, weather_data):

        with open(self.json_file, "w") as f:
            json.dump(self.weather_data, f)

        workbook = Workbook()
        sheet = workbook.active
        sheet.append(
            ["City", "Description", "Temperature", "Pressure", "Humidity"])
        for key, val in self.weather_data.items():
            data = [key, val["description"], val["temperature"],
                    val["pressure"], val["humidity"]]
            sheet.append(data)

        workbook.save(filename=self.excel_file)


weather_repository = WeatherRepository()
