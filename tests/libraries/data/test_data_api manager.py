import unittest
from unittest.mock import Mock, patch
from data.source.api.data_api_manager import DataAPIManager
from data.source.api.auth_strategies import AuthStrategy
from data.source.api.data_api_response_processors.api_response_processor import APIResponseProcessor


class TestDataAPIManager(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_data(self, mock_get):
        # Mocking the components
        mock_auth_strategy = Mock(spec=AuthStrategy)
        mock_auth_strategy.is_authenticated.return_value = True
        mock_auth_strategy.authenticate.return_value = 'token'

        mock_processor = Mock(spec=APIResponseProcessor)
        mock_processor.process_response.return_value = {'processed': 'data'}

        # Setting up the mocked response
        mock_response = Mock()
        mock_response.json.return_value = {'raw': 'data'}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # DataAPIManager instance
        manager = DataAPIManager(mock_auth_strategy, mock_processor)
        result = manager.fetch_data('https://api.example.com', 'endpoint')

        # Assertions
        mock_get.assert_called_with('https://api.example.com/endpoint', 
                                    headers={'Authorization': 'Bearer token'}, 
                                    params=None)
        self.assertEqual(result, {'processed': 'data'})

    @patch('data.source.file.file.File.save')
    def test_store_data(self, mock_save):
        # Mocking the components
        mock_auth_strategy = Mock(spec=AuthStrategy)
        mock_processor = Mock(spec=APIResponseProcessor)

        # DataAPIManager instance with mock components
        manager = DataAPIManager(mock_auth_strategy, mock_processor)
        
        # Dummy data and file paths
        data = {'some': 'data'}
        file_paths = ['path/to/file1.json', 'path/to/file2.json']
        
        # Call store_data method
        manager.store_data(data, file_paths)

        # Assertions
        mock_save.assert_any_call(data, 'path/to/file1.json')
        mock_save.assert_any_call(data, 'path/to/file2.json')
        self.assertEqual(mock_save.call_count, 2)

if __name__ == '__main__':
    unittest.main()