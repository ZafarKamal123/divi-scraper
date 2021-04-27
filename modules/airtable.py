from requests.exceptions import RequestException
from typing import Union
import requests
import json


class Airtable:
    """
        Handles api related calls
    """

    PROXY = "https://api.airtable.com/v0/appFKdswNrUeZ25Lm/Pages"
    api_key = "keyL7TsjgPHy6A6CT"

    @staticmethod
    def post_section(section):
        payload = {
            'fields': section,
            'typecast': True,
        }

        try:

            request_headers = {
                'Authorization': f"Bearer {Airtable.api_key}"
            }

            generated_proxy = "https://api.airtable.com/v0/appFKdswNrUeZ25Lm/DiviSections"
            response = requests.post(generated_proxy, headers=request_headers, json=payload)

            print(response.text)

            if response.status_code != 200:
                return False

        except RequestException as e:
            raise SystemExit('Failed to update section ', e)

        return True

    @staticmethod
    def get_layouts(offset="") -> Union[list, bool]:
        """ Will provide saved layouts from airtable 

        Returns:
            [list]: layouts
        """

        try:

            request_headers = {
                'Authorization': f"Bearer {Airtable.api_key}"
            }

            layout_offset = f"offset={offset}" if offset != "" else ""
            generated_proxy = Airtable.PROXY + "?" + layout_offset
            response = requests.get(generated_proxy, headers=request_headers)

            if response.status_code != 200:
                print(response.text)
                return False

            response_json = response.json()

            return [response_json.get('records'), response_json.get('offset')]

        except RequestException as e:
            raise SystemExit('Failed to get saved layout ', e)

    @staticmethod
    def post_layout(record) -> bool:

        payload = {
            'fields': {
                "Pack": record.get('pack'),
                "Page": record.get('page'),
                "Page Url": record.get('page_url'),
                "Page Code": record.get('page_code'),
                "Page ID": record.get('id'),
                "Niche": record.get('niche')
            },
            'typecast': True
        }
        request_headers = {
            'Authorization': f"Bearer {Airtable.api_key}"
        }

        try:
            response = requests.post(Airtable.PROXY, headers=request_headers, json=payload)

            if response.status_code == 200:
                print(f"page {record.get('page')} Successfully added to airtable!")
                return True
            else:
                print(response.text)
                return False

        except RequestException:
            print('Failed to post a record to airtable -> killing current process')
            return False
