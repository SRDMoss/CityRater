from db_init import collex, generate_cities
from openai import OpenAI
import json

client = OpenAI()

log_file_path = "error_log.txt"
def log_error(message, city_doc):
    with open(log_file_path, 'a', encoding='utf-8') as log_file:  # Specify UTF-8 encoding
        log_file.write(f"{message} - Document ID: {city_doc['_id']}, City: {city_doc['city']}, Admin: {city_doc['admin']}, ISO3: {city_doc['iso3']}\n")

# for city_doc in generate_cities():

    city_name, admin_name, iso3 = city_doc['city'], city_doc['admin'], city_doc['iso3']

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Output JSON."},
                {"role": "user", "content": f"Top two languages used in {city_name} ({admin_name}, {iso3}). Use '{city_name}' as key, languages as sub-keys, and the percentage (from 0.00 to 1.00) of common public interactions."}
            ]
        )
        content = json.loads(response.choices[0].message.content)
        languages = content.get(city_name, {})

        if not languages:  # Check if languages data is empty
            raise ValueError("No language data found for the API response.")

        sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        lang_1, lang_percent_1 = sorted_languages[0] if sorted_languages else ('None', 0)
        lang_2, lang_percent_2 = sorted_languages[1] if len(sorted_languages) > 1 else ('None', 0)

        update_result = collex.update_one(
            {'_id': city_doc['_id']}, 
            {'$set': {
                'lang_1': lang_1, 'lang_percent_1': lang_percent_1,
                'lang_2': lang_2, 'lang_percent_2': lang_percent_2
            }}
        )

        if update_result.matched_count == 0:
            raise ValueError("No document matched the update criteria.")
        elif update_result.modified_count == 0:
            raise ValueError("Document matched but was not modified.")

    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        log_error(error_message, city_doc)

for city_doc in generate_cities():

    city_name, admin_name, iso3 = city_doc['city'], city_doc['admin'], city_doc['iso3']

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Output JSON."},
                {"role": "user", "content": f"Continent of {city_name} ({admin_name}, {iso3}). 'continent' as key, 'North America','South America', 'Europe','Africa', 'Asia', 'Indonesia', or 'Antarctica' as value"}
            ]
        )

        content = json.loads(response.choices[0].message.content)
        continent = content.get('continent')

        if not continent:  # Check if languages data is empty
            raise ValueError("No continental data found for the API response.")


        update_result = collex.update_one({'_id': city_doc['_id']},{'$set': {'continent': continent}})

        if update_result.matched_count == 0:
            raise ValueError("No document matched the update criteria.")
        elif update_result.modified_count == 0:
            raise ValueError("Document matched but was not modified.")

    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        log_error(error_message, city_doc)



