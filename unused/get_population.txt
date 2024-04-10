import requests
from bs4 import BeautifulSoup
import re
from requests.exceptions import SSLError
import datetime
from pprint import pprint
import urllib.parse
import logging
import csv

logging.basicConfig(filename='example.log', level=logging.INFO)

class getPopulation: 
    def __init__(self, city_name):
        self.city_name = city_name

    def getPop(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }
        
        # Search for the city name on Google and extract the first search result URL
        google_url = f"https://www.google.com/search?q={self.city_name}+population"
        response = requests.get(google_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        search_results = soup.find_all('a', href=True)

        if search_results is not None:
            search_results = [x.get('href') for x in search_results if x.get('href') is not None and 'http' in x.get('href')]
            search_results = [x[x.find('http'):] for x in search_results if 'maps' not in x]
            search_results = [x[:x.find("&")] if "&" in x else x[:x.find("?")] if "?" in x else x for x in search_results]
            search_results = [x for x in search_results if 'wikipedia' in x]



        for site in search_results:
            # set up holders
            metroSave = []
            prefectureSave = []
            urbanSave = []
            otherSave = []            
            output = 'Output is secretly none.'
            logging.info(f"Site: {site}")
            try: 
                output = requests.get(site)
            except SSLError as e:
                print(f'Skipping {google_url} due to SSL error: \n\t {e}')
                continue
            except Exception as e:
                print(f'Error while processing {google_url}:  {e}')

            if output is not None:
                soup = BeautifulSoup(output.content, 'html.parser')
                trs = soup.find_all('tr')

                for tr in trs:
                    # assign label and data
                    label = tr.find('th', class_='infobox-label')
                    data = tr.find('td', class_='infobox-data')

                    # adjust data contents
                    if data:             
                        data = data.text.strip().replace(",", "")
                        if len(data) > 0:
                            data = data.split()[0]

                        # if the contents are a number in the right range
                        if data.isdigit() and (99999 < int(data) < 45000000):
                            if label:
                                label = label.text.strip()
                                logging.info(f"Accepted - {label}: {data}")
                                if 'metro' in label.lower():
                                    if len(label) == 5:
                                        metroSave = []
                                    else:
                                        metroSave.append(int(data))
                                elif 'prefecture' in label.lower():
                                    prefectureSave.append(int(data))
                                elif 'urban' in label.lower():
                                    urbanSave.append(int(data))
                                else:
                                    otherSave.append(int(data))

            population = next((x[0] for x in [prefectureSave, metroSave, urbanSave, otherSave] if len(x) > 0), None)
            logging.info("Population: " + str(population))         
            
            if population: 
                return population


