import unittest
from unittest.mock import patch, mock_open
from data.source.file.file import File
from data.source.file.file_handler_factory import FileHandlerFactory

class TestFile(unittest.TestCase):

    @patch('data.source.file.file_handler_factory.FileHandlerFactory.get_handler')
    def test_read(self, mock_get_handler):
        # Setup mock file handler
        mock_handler = mock_get_handler.return_value
        mock_handler.read.return_value = "test data"

        # Call the read method
        result = File.read('test.json')

        # Assertions
        mock_get_handler.assert_called_with('json', 'test.json')
        mock_handler.read.assert_called_once()
        self.assertEqual(result, "test data")

    @patch('data.source.file.file_handler_factory.FileHandlerFactory.get_handler')
    def test_save(self, mock_get_handler):
        # Setup mock file handler
        mock_handler = mock_get_handler.return_value
        mock_open_function = mock_open()

        with patch('builtins.open', mock_open_function):
            File.save("test data", ['test.json'])

        # Assertions
        mock_get_handler.assert_called_with('json', 'test.json')
        mock_handler.save.assert_called_once_with("test data")
        mock_open_function.assert_called_once_with('test.json', 'w')

if __name__ == '__main__':
    unittest.main()
