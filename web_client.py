"""Module for interacting with the Spoonacular API."""
from typing import Any, Dict, List

import requests


class SpoonacularClient(object):
    """
    Client for interacting with the Spoonacular API.

    Attributes:
        base_url (str): The base URL for the Spoonacular API.
        api_key (str): The API key used for authentication.
    """

    timeout: int = 30

    def __init__(self, api_key: str):
        """
        Initialize the SpoonacularClient.

        Args:
            api_key (str): The API key for authentication.
        """
        self.base_url = 'https://api.spoonacular.com/'
        self.api_key = api_key

    def get_recipes_by_ingredients(
        self, user_data: Dict[str, Any],
    ) -> dict:
        """
        Get recipes by ingredients.

        Args:
            user_data (Dict[str, Union[str, List[str]]):
            The data for the request.

        Returns:
            dict: Dictionary with recipe information.
        """
        user_data['apiKey'] = self.api_key
        response = requests.get(
            f'{self.base_url}recipes/findByIngredients',
            params=user_data,
            timeout=self.timeout,
        )
        if response.status_code == 200:
            id_list = [recipe['id'] for recipe in response.json()]
            return {'ids_of_recipes': id_list}
        print(f'Error! Status - {response.status_code}')
        return {'ids_of_recipes': ''}

    def get_taste_by_id_of_dish(self, dish_id: str) -> dict:
        """
        Get taste information by dish ID.

        Args:
            dish_id (str): The ID of the dish.

        Returns:
            dict: Dictionary with taste information.
        """
        response = requests.get(
            f'{self.base_url}recipes/{dish_id}/tasteWidget.json',
            params={'apiKey': self.api_key},
            timeout=self.timeout,
        )
        return response.json()

    def compute_glycemic_load(self, payload: Dict[str, List[str]]) -> dict:
        """
        Compute glycemic load.

        Args:
            payload (Dict[str, List[str]]): The payload for the request.

        Returns:
            dict: Dictionary with glycemic load information.
        """
        response = requests.post(
            f'{self.base_url}food/ingredients/glycemicLoad',
            json=payload,
            params={'apiKey': self.api_key},
            timeout=self.timeout,
        )
        return response.json()


api_key = '6970f7110b5948bcabf091a25eff8b24'
spoonacular_client = SpoonacularClient(api_key)
data_for_request = {'ingredients': 'sugar', 'number': '3'}
recipes = spoonacular_client.get_recipes_by_ingredients(data_for_request)
taste_of_dish = spoonacular_client.get_taste_by_id_of_dish('635315')
glycemic_load = spoonacular_client.compute_glycemic_load(
    {'ingredients': ['1 kiwi', '2 cups rice', '2 glasses of water']},
)
