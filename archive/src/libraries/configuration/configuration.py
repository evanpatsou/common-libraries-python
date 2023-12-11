# configuration.py
from config_strategy import ConfigStrategy

class ConfigurationError(Exception):
    """Custom exception class for Configuration errors."""
    pass

class Configuration:
    """Main class for application configuration management."""

    def __init__(self, strategies: list[ConfigStrategy] = None):
        """Initializes the Configuration instance.

        Args:
            strategies (list[ConfigStrategy], optional): List of configuration reading strategies.
        """
        self.strategies = strategies or []
        self.config_data = {}

    def load(self) -> None:
        """Loads configurations using the added strategies.

        Raises:
            ConfigurationError: If an error occurs during loading of configurations.
        """
        for strategy in self.strategies:
            try:
                new_config = strategy.read_config()
                self._merge_config(new_config)
            except Exception as e:
                raise ConfigurationError(f"Failed to load configuration: {e}")

    def _merge_config(self, new_config: dict) -> None:
        """Merges a new configuration into the existing configuration data.

        Args:
            new_config (dict): The new configuration to merge.
        """
        self.config_data.update(new_config)

    def add_dict_config(self, dict_config: dict) -> None:
        """Adds a new dictionary configuration.

        Args:
            dict_config (dict): Configuration dictionary to add.
        """
        self._merge_config(dict_config)

    def get_config(self) -> dict:
        """Retrieves the entire merged configuration.

        Returns:
            dict: The merged configuration data.
        """
        return self.config_data

    def get(self, key: str, default=None):
        """Retrieves a value from the configuration.

        Args:
            key (str): The key of the configuration value to retrieve.
            default: The default value to return if the key is not found.

        Returns:
            The value associated with the key, or the default value if the key is not found.
        """
        return self.config_data.get(key, default)
