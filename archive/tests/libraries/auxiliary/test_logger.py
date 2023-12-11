import unittest
import logging
import tempfile
import os
from logger import Logger  # Assuming the Logger class is in logger.py

class TestLogger(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for logging
        self.temp_log_file = tempfile.NamedTemporaryFile(delete=False)
        self.log_file_name = self.temp_log_file.name
        self.temp_log_file.close()

        # Initialize Logger with the temporary file
        self.logger = Logger.get_instance(log_file=self.log_file_name, log_level=logging.DEBUG, file_logging=True, console_logging=False)

    def tearDown(self):
        # Delete the temporary log file after testing
        os.remove(self.log_file_name)
        Logger.instance = None  # Reset the Logger instance for the next test

    def test_logging_to_file(self):
        self.logger.log("Test message", level=logging.INFO)
        with open(self.log_file_name, 'r') as f:
            self.assertIn("INFO - Test message", f.read())

    def test_logging_with_different_levels(self):
        self.logger.log("Debug message", level=logging.DEBUG)
        self.logger.log("Warning message", level=logging.WARNING)
        with open(self.log_file_name, 'r') as f:
            log_content = f.read()
            self.assertIn("DEBUG - Debug message", log_content)
            self.assertIn("WARNING - Warning message", log_content)

    def test_logging_exception(self):
        try:
            raise ValueError("Test exception")
        except Exception as e:
            with self.assertRaises(SystemExit):
                self.logger.log_exception(e)

        with open(self.log_file_name, 'r') as f:
            self.assertIn("ERROR - Exception occurred: Test exception", f.read())

    def test_disabled_logging(self):
        disabled_logger = Logger.get_instance(disabled=True)
        disabled_logger.log("This should not be logged", level=logging.INFO)
        self.assertFalse(os.path.exists(self.log_file_name))

    def test_console_logging_only(self):
        console_logger = Logger.get_instance(log_file=None, console_logging=True, file_logging=False)
        console_logger.log("Console only message", level=logging.INFO)
        self.assertFalse(os.path.exists(self.log_file_name))  # No file should be created

if __name__ == '__main__':
    unittest.main()
