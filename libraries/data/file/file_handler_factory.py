from typing import Dict, Type
from .handlers import AbstractFileHandler, JSONFileHandler, CSVFileHandler

class FileHandlerFactory:
    """
    A factory for creating file handlers based on the file type.

    Attributes:
        handlers (Dict[str, Type[AbstractFileHandler]]): A dictionary mapping file extensions 
                                                         to file handler classes.
    """

    def __init__(self) -> None:
        """Initializes the FileHandlerFactory with a mapping of file types to handlers."""
        self.handlers: Dict[str, Type[AbstractFileHandler]] = {
            'json': JSONFileHandler,
            'csv': CSVFileHandler,
            # Add more file types and their corresponding handlers here
        }

    def get_handler(self, file_type: str, filename: str) -> AbstractFileHandler:
        """
        Gets a file handler based on the file type.

        Args:
            file_type (str): The type of the file (e.g., 'json', 'csv').
            filename (str): The name of the file.

        Returns:
            AbstractFileHandler: An instance of the file handler suitable for the file type.

        Raises:
            ValueError: If the file type is not supported.
        """
        handler_class = self.handlers.get(file_type)
        if handler_class:
            return handler_class(filename)
        else:
            raise ValueError(f"Unsupported file type: '{file_type}'")
