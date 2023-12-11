# test_configuration.py
import unittest
from unittest.mock import Mock

from src.libraries.configuration import ConfigStrategy
from src.libraries.configuration import Configuration, ConfigurationError


class TestConfiguration(unittest.TestCase):
    """Tests for the Configuration class."""

    def test_loading_configurations(self):
        """Test loading configurations using strategies."""
        mock_json_strategy = Mock(spec=ConfigStrategy)
        mock_json_strategy.read_config.return_value = {"json_key": "json_value"}

        mock_csv_strategy = Mock(spec=ConfigStrategy)
        mock_csv_strategy.read_config.return_value = {"csv_key": "csv_value"}

        config = Configuration([mock_json_strategy, mock_csv_strategy])
        config.load()

        expected_config = {
            "json_key": "json_value",
            "csv_key": "csv_value"
        }
        self.assertEqual(config.get_config(), expected_config)

    def test_adding_dict_configuration(self):
        """Test adding a dictionary configuration."""
        config = Configuration()
        config.add_dict_config({"dict_key": "dict_value"})

        self.assertEqual(config.get("dict_key"), "dict_value")

    def test_merging_configurations(self):
        """Test merging of configurations from different sources."""
        config = Configuration()
        config.add_dict_config({"key1": "value1"})
        config.add_dict_config({"key2": "value2"})

        expected_config = {
            "key1": "value1",
            "key2": "value2"
        }
        self.assertEqual(config.get_config(), expected_config)

    def test_error_handling_during_loading(self):
        """Test error handling during configuration loading."""
        mock_faulty_strategy = Mock(spec=ConfigStrategy)
        mock_faulty_strategy.read_config.side_effect = Exception("Read error")

        config = Configuration([mock_faulty_strategy])
        
        with self.assertRaises(ConfigurationError):
            config.load()

if __name__ == '__main__':
    unittest.main()
