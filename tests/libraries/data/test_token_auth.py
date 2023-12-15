import unittest
from unittest.mock import patch
from data.source.api.auth_strategies import ManualTokenAuth, EndpointTokenAuth

class TestManualTokenAuth(unittest.TestCase):

    def test_authenticate(self):
        auth = ManualTokenAuth("test-token")
        self.assertEqual(auth.authenticate(), "test-token")

class TestEndpointTokenAuth(unittest.TestCase):

    @patch('requests.post')
    def test_authenticate(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.json.return_value = {'token': 'endpoint-token'}
        auth = EndpointTokenAuth("http://api.example.com/auth", {"username": "user", "password": "pass"})
        self.assertEqual(auth.authenticate(), "endpoint-token")

if __name__ == '__main__':
    unittest.main()
