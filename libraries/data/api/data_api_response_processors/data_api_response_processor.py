from abc import ABC, abstractmethod
from typing import Any

class APIResponseProcessor(ABC):
    """
    Abstract base class for API response processors.

    Implementations of this class should provide methods to process
    different API responses into a standardized format.
    """

    @abstractmethod
    def process_response(self, response: Any) -> Any:
        """
        Processes the API response.

        Args:
            response (Any): The raw response from the API.

        Returns:
            Any: The processed data.
        """
        pass
