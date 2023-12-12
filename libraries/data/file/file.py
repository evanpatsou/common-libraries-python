# data/source/file/file.py

from pathlib import Path
from typing import Any, List
from .file_handler_factory import FileHandlerFactory

class File:
    """
    Class to handle file operations, including reading from and writing to files.

    Methods:
        read: Reads data from a specified file path.
        save: Saves data to a list of specified file paths.
    """

    @staticmethod
    def read(file_path: str) -> Any:
        """
        Reads data from the specified file.

        Args:
            file_path (str): The path of the file to read from.

        Returns:
            Any: The data read from the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If the file read fails.
        """
        path = Path(file_path)
        factory = FileHandlerFactory()
        handler = factory.get_handler(path.suffix.lstrip('.'), file_path)
        return handler.read()

    @staticmethod
    def save(data: Any, output_paths: List[str]) -> None:
        """
        Saves data to the specified file paths.

        Args:
            data (Any): The data to be saved.
            output_paths (List[str]): The file paths to save the data to.

        Raises:
            IOError: If the file write fails.
        """
        factory = FileHandlerFactory()
        for path_str in output_paths:
            path = Path(path_str)
            handler = factory.get_handler(path.suffix.lstrip('.'), path_str)
            handler.save(data)
