from get_population import *
from import_cities import *
from collections import defaultdict as dd
from pprint import pprint
import csv


# get list of all cities in the world over 100k population from csv
filename = "worldcities.csv"
cities = []
inputFile = getCitiesFromFile(filename, cities)
cities = inputFile.getCities()

with open('errorCities.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['time', 'city', 'population'])

with open('output.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for city in cities:
        cityPop = getPopulation(city)
        pop = cityPop.getPop()
        if not pop:
            with open('error_cities.txt', 'a') as g:
                now = datetime.datetime.now() 
                nowForm = now.strftime("%Y-%m-%d %H:%M:%S")
                print(nowForm + ":  " + self.city_name)
                print(nowForm + ":  " + self.city_name, file=g)  
        else:
            writer.writerow([city, pop])
            breaker = ": "
            if len(city) < 30:
                breaker += "\t"
            if len(city) < 22:
                breaker += "\t"
            if len(city) < 14:
                breaker += "\t"
            if len(city) < 6:
                breaker += "\t"
            print(city + breaker + str(pop))
