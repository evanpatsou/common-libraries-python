from pathlib import Path

class PathBuilder:
    def __init__(self, *path_components):
        """
        Initialize the PathBuilder with initial path components.

        Args:
            path_components (str): Initial components of the path.
        """
        self.path = Path(*path_components)

    def add(self, *path_components):
        """
        Add more components to the path.

        Args:
            path_components (str): Additional components to be added to the path.

        Returns:
            PathBuilder: The instance of PathBuilder for method chaining.
        """
        self.path = self.path.joinpath(*path_components)
        return self

    def create(self):
        """
        Create the directory if it doesn't exist.
        """
        self.path.mkdir(parents=True, exist_ok=True)

    @property
    def get_path(self):
        """
        Return the current path without creating it.

        Returns:
            pathlib.Path: The current path.
        """
        return self.path

    def __str__(self):
        """
        String representation of the path.

        Returns:
            str: The string representation of the current path.
        """
        return str(self.path)
