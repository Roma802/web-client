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

    def get_response(
        self,
        user_method: str,
        rest_url: str,
        user_data: Dict[str, Any] = None,
        request_payload: Dict[str, List[str]] = None,
    ) -> requests.Response:
        """
        Get the API response for a given URL.

        Args:
            user_method (str): The method for the request ('get' or 'post').
            rest_url (str): The specific endpoint of the Spoonacular API.
            user_data (Dict[str, Any], optional): Additional data for request.
            request_payload (Dict[str, List[str]], optional): data for request

        Returns:
            requests.Response: The response object from the API request.
        """
        if user_data is None:
            user_data = {}
        user_data['apiKey'] = self.api_key
        if user_method == 'get':
            return requests.get(
                f'{self.base_url}{rest_url}',
                params=user_data,
                timeout=self.timeout,
            )
        elif user_method == 'post':
            return requests.post(
                f'{self.base_url}{rest_url}',
                params=user_data,
                json=request_payload,
                timeout=self.timeout,
            )


class SpoonacularGetClient(SpoonacularBaseClient):
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
        response = self.get_response(
            'get',
            'recipes/findByIngredients',
            user_data,
        )
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
        response = self.get_response(
            'get',
            f'recipes/{dish_id}/tasteWidget.json',
        )
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
        response = self.get_response(
            'post',
            'food/ingredients/glycemicLoad',
            request_payload=payload,
        )
        return response.json()


class SpoonacularNasaClient(SpoonacularPostClient, SpoonacularGetClient):
    """Client for interacting with the Spoonacular API."""

    pass


api_key = '6970f7110b5948bcabf091a25eff8b24'
spoonacular_client = SpoonacularNasaClient(api_key)
data_for_request = {'ingredients': 'sugar', 'number': '3'}
recipes = spoonacular_client.get_recipes_by_ingredients(data_for_request)
taste_of_dish = spoonacular_client.get_taste_by_id_of_dish('635315')
glycemic_load = spoonacular_client.compute_glycemic_load(
    {'ingredients': ['1 kiwi', '2 cups rice', '2 glasses of water']},
)
