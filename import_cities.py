import csv
import urllib.parse
from unidecode import unidecode
from pprint import pprint

class getCitiesFromFile: 
    def __init__(self, file, cities):
        self.file = file
        self.cities = []

    def getCities(self):
        with open(self.file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['population'].isdigit() and int(row['population']) > 100000:
                    city = row['city_ascii']
                    self.cities.append(city)
        return self.cities
