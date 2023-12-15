import requests
from typing import Any, Dict, List
from .auth_strategies import AuthStrategy
from .data_api_response_processors.api_response_processor import APIResponseProcessor
from data.source.file.file import File

class DataAPIManager:
    """
    Manages interactions with external APIs, handling authentication, data retrieval,
    and response processing.
    """

    def __init__(self, auth_strategy: AuthStrategy, response_processor: APIResponseProcessor) -> None:
        """
        Initializes the DataAPIManager with an authentication strategy and a response processor.

        Args:
            auth_strategy (AuthStrategy): The authentication strategy for API access.
            response_processor (APIResponseProcessor): The processor for handling API responses.
        """
        self.auth_strategy = auth_strategy
        self.response_processor = response_processor

    def fetch_data(self, base_url: str, endpoint: str, params: Dict[str, Any] = None) -> Any:
        """
        Fetches data from the specified API endpoint and processes the response.

        Args:
            base_url (str): The base URL of the API.
            endpoint (str): The API endpoint to fetch data from.
            params (Dict[str, Any], optional): Query parameters to include in the request.

        Returns:
            Any: The processed data returned by the API.

        Raises:
            requests.RequestException: If the request to the API fails.
        """
        if not self.auth_strategy.is_authenticated():
            self.auth_strategy.authenticate()

        headers = {'Authorization': f'Bearer {self.auth_strategy.authenticate()}'}
        full_url = f'{base_url}/{endpoint}'
        response = requests.get(full_url, headers=headers, params=params)
        response.raise_for_status()

        return self.response_processor.process_response(response.json())

    def store_data(self, data: Any, file_paths: List[str]) -> None:
        """
        Stores the given data in the specified file paths.

        Args:
            data (Any): The data to be stored.
            file_paths (List[str]): A list of file paths where the data should be stored.
        """
        for path in file_paths:
            File.save(data, path)
