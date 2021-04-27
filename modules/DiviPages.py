from modules.airtable import Airtable
from functions import overwrite_file
from paths import *
import requests
import json


class DiviPages:
    base_url = "https://www.elegantthemes.com/"
    api_key = "498d640c4a3fccb30f468cc4743c331c3e8dd3b2"
    user_name = "munirkamal"
    nonce = "ad71a46d54"

    @staticmethod
    def get_page_code(url):
        response = requests.get(url)
        response_json = response.json()

        return response_json

    @staticmethod
    def update_pages():

        with open(DIVI_DATA_PATH, 'r+') as data_file:

            data_json = json.load(data_file)

            # divi layout pages
            layouts = data_json.get('layouts')

            for layout in layouts:

                layout_id, layout_name, url, layout_categories = layout.get('id'), layout.get('name'), layout.get(
                    'url'), layout.get('categories')

                with open(DIVI_PROGRESS_PATH, 'r+') as progress_file:
                    current_progress = json.load(progress_file)

                    if layout_id in current_progress:
                        continue

                    progress_file.close()

                download_query = f"/download?et_username={DiviPages.user_name}&et_api_key={DiviPages.api_key}&nonce={DiviPages.nonce}"
                download_url = DiviPages.base_url + url + download_query

                layout_data = {
                    'pack': layout.get('pack'),
                    'page': layout_name,
                    'page_url': DiviPages.base_url + url,
                    'page_code': download_url,
                    'niche': layout_categories,
                    "id": layout_id
                }

                post_status = Airtable.post_layout(layout_data)

                if post_status != True:
                    # this means that post failed
                    raise SystemExit('Something wrong happened')
                else:
                    # updating current progress in the progress file
                    with open(DIVI_PROGRESS_PATH, 'r+') as progress_file:

                        current_progress = json.load(progress_file)
                        current_progress.append(layout_id)
                        overwrite_file(progress_file, json.dumps(current_progress))

                        progress_file.close()
s