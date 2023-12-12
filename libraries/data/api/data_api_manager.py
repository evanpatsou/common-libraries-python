# data/source/api/data_api_manager.py

import requests
from requests.exceptions import RequestException
from data.source.file.file_handler_factory import FileHandlerFactory
from .auth_strategies import AuthStrategy
from exceptions.custom_exceptions import DataFetchError, FileSaveError
from typing import Any, List
import logging

class DataAPIManager:
    """Manages API interactions and data storage.

    This class handles fetching data from an API using a specified authentication
    strategy and storing the data in files using a file handler factory.

    Attributes:
        base_url (str): Base URL of the API.
        auth_strategy (AuthStrategy): The authentication strategy to use.
        file_factory (FileHandlerFactory): A factory for creating file handlers.
    """

    def __init__(self, base_url: str, auth_strategy: AuthStrategy) -> None:
        """Initializes the DataAPIManager with a base URL and an authentication strategy.

        Args:
            base_url (str): The base URL of the API.
            auth_strategy (AuthStrategy): The authentication strategy.
        """
        self.base_url = base_url
        self.auth_strategy = auth_strategy
        self.file_factory = FileHandlerFactory()

    def fetch_data(self, endpoint: str) -> Any:
        """Fetches data from a specific API endpoint.

        Args:
            endpoint (str): The API endpoint to fetch data from.

        Returns:
            Any: The data returned by the API.

        Raises:
            DataFetchError: If the request to the API fails.
        """
        try:
            if not self.auth_strategy.is_authenticated():
                self.auth_strategy.authenticate()

            headers = {'Authorization': f'Bearer {self.auth_strategy.authenticate()}'}
            response = requests.get(f'{self.base_url}/{endpoint}', headers=headers)
            response.raise_for_status()
            return response.json()

        except RequestException as e:
            logging.error(f"Error fetching data from API: {e}")
            raise DataFetchError(f"Failed to fetch data from {endpoint}")

    def store_data(self, data: Any, file_paths: List[str]) -> None:
        """Stores the given data in the specified files.

        Args:
            data (Any): The data to be stored.
            file_paths (List[str]): A list of file paths where the data should be stored.

        Raises:
            FileSaveError: If saving the data to any of the files fails.
        """
        for path in file_paths:
            try:
                file_type = path.split('.')[-1]
                file_handler = self.file_factory.get_handler(file_type, path)
                file_handler.save(data)
            except IOError as e:
                logging.error(f"Error saving data to file {path}: {e}")
                raise FileSaveError(f"Failed to save data to {path}")
