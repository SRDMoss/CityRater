import json 
from modules.pywwo import setKey, LocalWeather
from modules.config import OWW_API_KEY
from modules.db_init import generate_cities


# def update_from_csv(csv_file_path, region_level):

#     # create list to store error regions if there are any
#     csv_errors = []

#     # Open the CSV file for reading
#     with open(csv_file_path, mode="r", encoding="utf-8") as csvfile:

#         # Create a CSV reader object
#         csv_reader = csv.DictReader(csvfile)

#         # Get all headings present in first line of csv
#         key_list = csv_reader.fieldnames

#         # Iterate over each row in the CSV
#         for row in csv_reader:

#             # Extract region name from the CSV row
#             region_name = row[region_level]
#             filter_criteria = {region_level: region_name}

#             # If there is no match, document it
#             if collex.count_documents({region_level: region_name}) == 0:
#                 print(f"No data for {region_level}: {region_name}")
#                 csv_errors.append((region_level, region_name)) # Pack a tuple and collect it for documentation.
#                 continue

#             # Create dictionary for updates
#             update_dict = {key: row[key] for key in key_list if key != region_level}
            
#             # Update mongo db
#             outcome = collex.update_many(filter_criteria, {"$set": update_dict})

#             print(f"Updated {outcome.modified_count} documents for {region_level}: {region_name}")

#     # Document any collected errors. 
#     if len(csv_errors) > 0: 
#         with open("errors_by_region.txt", mode="w") as errorfile:
#             for region, name in csv_errors:  # Unpack the tuple
#                 errorfile.write(f"{region}: {name}\n")


# Initial cities with population import
cities_path = "./resources/health.csv"
cities_level = "city_ascii"
# update_from_csv(cities_path, cities_level)

# Adding Healthcare Data
health_path = "./resources/health.csv"
health_level = "country"
# update_from_csv(health_path, health_level)
                
# Adding legal data        
legal_path = "./resources/legal_data.csv"
legal_level = "country"
# update_from_csv(legal_path, legal_level)

# Adding government data
gov_path = "./resources/gov_system.csv"
gov_level = "country"
# update_from_csv(gov_path, gov_level)

# documents = collex.find()

# field_names = set()
# for doc in documents:
#     field_names.update(doc.keys())

# field_names_list = list(field_names)

# with open("fieldnames.txt", mode="w") as fieldfile: 
#     for name in field_names: 
#         fieldfile.write(name + '\n')

# collex.update_many({"open_in_military": "NA  "}, {"$set": {"open_in_military": "No Army"}})
# collex.update_many({"same_sex_sexual_attraction": 1000}, {"$set": {"same_sex_sexual_attraction": "Prohibited"}})

setKey(OWW_API_KEY)

# Initialize a list to hold all the data
all_data = []

for city in generate_cities():

    location = f"{city['lat']},{city['lon']}"

    result = LocalWeather(q=location, fx="no", cc="no", mca="yes", format="json")
    
    # Extract the data for the current city
    data = result.data['data']['ClimateAverages'][0]['month']
    
    # Append a new object containing the city name and its data
    all_data.append({
        'city': city['city'],
        'data': data
    })

# File path where you want to save the data
file_path = 'E:/Projects/Leftover assets/cities_weather_data.json'

# Write the collected data to a JSON file
with open(file_path, 'w') as file:
    json.dump(all_data, file, indent=1)

print("Data saved to 'cities_weather_data.json'")


