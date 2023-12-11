# test_python_config_strategy.py
import unittest
import tempfile
from config_strategy import PythonConfigStrategy

class TestPythonConfigStrategy(unittest.TestCase):
    """Tests for the PythonConfigStrategy class."""

    def test_read_config(self):
        """Test reading configuration from a Python file."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.py') as temp_file:
            temp_file.write("""
class AppConfig:
    general_path = 'path/to/something'
    class DatabaseConfig:
        uri = 'sqlite:///example.db'
        pool_size = 5
""")
            temp_file.flush()
            strategy = PythonConfigStrategy(temp_file.name)
            config = strategy.read_config()
            expected_config = {
                'general_path': 'path/to/something',
                'DatabaseConfig': {
                    'uri': 'sqlite:///example.db', 
                    'pool_size': 5
                }
            }
            self.assertEqual(config, expected_config)

if __name__ == '__main__':
    unittest.main()
