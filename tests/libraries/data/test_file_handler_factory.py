import unittest
from data.source.file.file_handler_factory import FileHandlerFactory
from data.source.file.handlers import JSONFileHandler, CSVFileHandler

class TestFileHandlerFactory(unittest.TestCase):

    def setUp(self):
        """Set up the FileHandlerFactory instance for testing."""
        self.factory = FileHandlerFactory()

    def test_get_handler_json(self):
        """Test that the factory returns a JSONFileHandler for 'json' files."""
        handler = self.factory.get_handler('json', 'test.json')
        self.assertIsInstance(handler, JSONFileHandler)

    def test_get_handler_csv(self):
        """Test that the factory returns a CSVFileHandler for 'csv' files."""
        handler = self.factory.get_handler('csv', 'test.csv')
        self.assertIsInstance(handler, CSVFileHandler)

    def test_get_handler_unsupported(self):
        """Test that the factory raises ValueError for unsupported file types."""
        with self.assertRaises(ValueError):
            self.factory.get_handler('unsupported', 'test.unsupported')

if __name__ == '__main__':
    unittest.main()
