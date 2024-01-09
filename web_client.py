"""Module for interacting with the Spoonacular API."""
from typing import Any, Dict, List

import requests


class SpoonacularBaseClient(object):
    """
    Base class for inheritance.

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


class SpoonacularBaseGetClient(SpoonacularBaseClient):
    """
    Client for interacting with the GET methods of Spoonacular API.

    Attributes:
        base_url (str): The base URL for the Spoonacular API.
        api_key (str): The API key used for authentication.

    Methods:
        get_response(self, rest_url: str, user_data:
        Dict[str, Any] = None) -> requests.Response:
        Get the API response for a given URL.

        Args:
            rest_url (str): The specific endpoint of the Spoonacular API.
            user_data (Dict[str, Any], optional):
            Additional data for the request. Defaults to None.

        Returns:
            requests.Response: The response object from the API request.
    """

    def get_response(
        self, rest_url: str, user_data: Dict[str, Any] = None,
    ) -> requests.Response:
        """
        Get the API response for a given URL.

        Args:
            rest_url (str): The specific endpoint of the Spoonacular API.
            user_data (Dict[str, Any], optional):
            Additional data for the request. Defaults to None.

        Returns:
            requests.Response: The response object from the API request.
        """
        if user_data is None:
            user_data = {}
        user_data['apiKey'] = self.api_key
        return requests.get(
            f'{self.base_url}{rest_url}',
            params=user_data,
            timeout=self.timeout,
        )


class SpoonacularGetClient(SpoonacularBaseGetClient):
    """Client for interacting with the GET methods of Spoonacular API."""

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
        response = self.get_response('recipes/findByIngredients', user_data)
        if response.status_code == requests.codes.ok:
            id_list = [recipe['id'] for recipe in response.json()]
            return {'ids_of_recipes': id_list}
        return {'ids_of_recipes': ''}

    def get_taste_by_id_of_dish(self, dish_id: str) -> dict:
        """
        Get taste information by dish ID.

        Args:
            dish_id (str): The ID of the dish.

        Returns:
            dict: Dictionary with taste information.
        """
        response = self.get_response(f'recipes/{dish_id}/tasteWidget.json')
        return response.json()


class SpoonacularPostClient(SpoonacularBaseClient):
    """Client for interacting with the Spoonacular API."""

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
spoonacular_get_client = SpoonacularGetClient(api_key)
spoonacular_post_client = SpoonacularPostClient(api_key)
data_for_request = {'ingredients': 'sugar', 'number': '3'}
recipes = spoonacular_get_client.get_recipes_by_ingredients(data_for_request)
taste_of_dish = spoonacular_get_client.get_taste_by_id_of_dish('635315')
glycemic_load = spoonacular_post_client.compute_glycemic_load(
    {'ingredients': ['1 kiwi', '2 cups rice', '2 glasses of water']},
)
