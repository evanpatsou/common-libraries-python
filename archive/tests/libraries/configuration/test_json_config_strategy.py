# test_json_config_strategy.py
import unittest
import tempfile
import json
from config_strategy import JSONConfigStrategy

class TestJSONConfigStrategy(unittest.TestCase):
    """Tests for the JSONConfigStrategy class."""

    def test_read_config(self):
        """Test reading configuration from a JSON file."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp_file:
            json.dump({"json_key": "json_value"}, temp_file)
            temp_file.flush()
            strategy = JSONConfigStrategy(temp_file.name)
            config = strategy.read_config()
            self.assertEqual(config, {"json_key": "json_value"})

if __name__ == '__main__':
    unittest.main()
