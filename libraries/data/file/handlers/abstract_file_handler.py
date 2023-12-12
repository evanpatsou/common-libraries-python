from abc import ABC, abstractmethod
from typing import Any

class AbstractFileHandler(ABC):
    """
    Abstract base class for file handlers.

    This class defines a common interface for all file handlers to implement
    methods for reading from and writing to files.

    Attributes:
        filename (str): The name of the file to be handled.
    """

    def __init__(self, filename: str) -> None:
        """
        Initializes the file handler with a filename.

        Args:
            filename (str): The name of the file to be handled.
        """
        self.filename = filename

    @abstractmethod
    def read(self) -> Any:
        """
        Reads data from a file.

        Returns:
            Any: The data read from the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If the file read fails.
        """
        pass

    @abstractmethod
    def save(self, data: Any) -> None:
        """
        Saves data to a file.

        Args:
            data (Any): The data to be saved.

        Raises:
            IOError: If the file write fails.
        """
        pass
