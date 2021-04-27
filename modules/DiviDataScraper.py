from requests.exceptions import RequestException
from functions import overwrite_file
from bs4 import BeautifulSoup
from locators.divi import *
from paths import *
import requests


class DataScraper:
    url = "https://www.elegantthemes.com/layouts/"

    """

        Will handle divi page scraping part
    
    """

    @staticmethod
    def save_updated_data():

        try:

            response = requests.get(DataScraper.url)
            soup = BeautifulSoup(response.text, "html.parser")
            global_script = soup.find('script', {'id': 'et-dlib-app-js-before'})

            global_script = str(global_script)
            data_json = global_script[87:len(global_script) - 11]

            with open(DIVI_DATA_PATH, 'r+') as data_file:
                # overwriting data
                overwrite_file(data_file, data_json)
                # closing the file
                data_file.close()

        except RequestException:
            print("Failed to get json data!!")

        except ValueError:
            raise SystemExit("Failed to parse Divi JSON!!")
