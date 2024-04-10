import csv

class getDataFromFile: 
    def __init__(self, file):
        self.file = file
    
    def get_cities(self):
        with open(self.file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['population'].isdigit() and int(row['population']) > 100000:
                    city = row['city_ascii']
                    admin = row['admin_name']
                    country = row['country']
                    iso2 = row['iso2']
                    iso3 = row['iso3']
                    lat = row['lat']
                    lon = row['lng']
                    population = row['population']
                    yield {
                        'city': city,
                        'admin': admin,
                        'country': country,
                        'iso2': iso2,
                        'iso3': iso3,
                        'lat': lat,
                        'lon': lon,
                        'population': population
                    }
