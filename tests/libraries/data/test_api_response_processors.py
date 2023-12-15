import unittest
from data.source.api.data_api_response_processors.api_response_processor import APIResponseProcessor
from data.source.api.data_api_response_processors.json_response_processor import JSONResponseProcessor

class TestJSONResponseProcessor(unittest.TestCase):

    def test_process_response(self):
        processor = JSONResponseProcessor()
        raw_response = {"key": "value"}
        processed_response = processor.process_response(raw_response)
        self.assertEqual(processed_response, raw_response)  # assuming simple processing

if __name__ == '__main__':
    unittest.main()
