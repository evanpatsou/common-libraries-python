class PythonConfigStrategy(ConfigStrategy):
    """Strategy for reading structured Python file configuration."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_config(self) -> dict:
        """Loads a Python file and extracts configuration data from the first found class and its nested classes.

        Returns:
            dict: Configuration data read from the Python file.
        """
        with open(self.file_path, 'r') as file:
            namespace = {}
            exec(file.read(), {}, namespace)

        # Find the first class defined in the file
        config_class = next((obj for obj in namespace.values() if isinstance(obj, type)), None)
        if not config_class:
            raise ValueError("No configuration class found in the file.")

        return self._process_config_class(config_class)

    def _process_config_class(self, class_obj) -> dict:
        """Processes a configuration class and its nested classes.

        Args:
            class_obj (class): The class object to process.

        Returns:
            dict: Extracted configuration data.
        """
        config_data = {}
        for attr_name in dir(class_obj):
            if not attr_name.startswith('_'):
                attr_value = getattr(class_obj, attr_name)
                if isinstance(attr_value, type):  # Nested class
                    config_data[attr_name] = self._extract_class_attributes(attr_value)
                else:  # Top-level attribute
                    config_data[attr_name] = attr_value
        return config_data

    def _extract_class_attributes(self, class_obj) -> dict:
        """Extracts attributes from a class, excluding callable methods and private attributes.

        Args:
            class_obj (class): The class object to extract attributes from.

        Returns:
            dict: Dictionary of attributes and their values.
        """
        return {attr: getattr(class_obj, attr) for attr in dir(class_obj) 
                if not callable(getattr(class_obj, attr)) and not attr.startswith('_')}
