# test_csv_config_strategy.py
import unittest
import tempfile
import csv
from config_strategy import CSVConfigStrategy

class TestCSVConfigStrategy(unittest.TestCase):
    """Tests for the CSVConfigStrategy class."""

    def test_read_config(self):
        """Test reading configuration from a CSV file."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as temp_file:
            writer = csv.writer(temp_file)
            writer.writerow(["key", "value"])
            writer.writerow(["csv_key", "csv_value"])
            temp_file.flush()
            strategy = CSVConfigStrategy(temp_file.name)
            config = strategy.read_config()
            self.assertEqual(config, [{"key": "csv_key", "value": "csv_value"}])

if __name__ == '__main__':
    unittest.main()
