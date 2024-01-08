import json
from typing import Dict

import requests


class SpoonacularClient:
    def __init__(self, api_key):
        self.base_url = 'https://api.spoonacular.com/'
        self.api_key = api_key

    def get_recipes_by_ingridients(self, data: Dict[str, str]):
        data['apiKey'] = self.api_key
        try:
            response = requests.get(f"{self.base_url}recipes/findByIngredients", params=data, timeout=30)
            if response.status_code == 200:
                id_list = [item['id'] for item in response.json()]
                return {'ids_of_recipes': id_list}
            else:
                return f'Error! Status error - {response.status_code}'
        except requests.RequestException as e:
            return f'Request failed with exception: {e}'

    def get_taste_by_id_of_dish(self, id):
        data['apiKey'] = self.api_key
        try:
            response = requests.get(f"{self.base_url}recipes/{id}/tasteWidget.json", params=data, timeout=30)
            return response.json()
        except requests.RequestException as e:
            return f'Request failed with exception: {e}'

    def compute_glycemic_load(self, payload):
        try:
            response = requests.post(f"{self.base_url}food/ingredients/glycemicLoad?apiKey={self.api_key}",
                                     json=payload,
                                     timeout=30)
            return response.json()
        except requests.RequestException as e:
            return f'Request failed with exception: {e}'


api_key = '6970f7110b5948bcabf091a25eff8b24'
spoonacular_client = SpoonacularClient(api_key)
data = {'ingredients': 'sugar', 'number': '3'}
print(spoonacular_client.get_recipes_by_ingridients(data))
print(spoonacular_client.get_taste_by_id_of_dish('635315'))
print(spoonacular_client.compute_glycemic_load({"ingredients": ["1 kiwi", "2 cups rice", "2 glasses of water"]}))

