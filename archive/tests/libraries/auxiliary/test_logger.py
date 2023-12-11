import unittest
import os
import logging
from logger import Logger  # Assuming the Logger class is in logger.py

class TestLogger(unittest.TestCase):

    def setUp(self):
        self.log_file = 'test_log.txt'
        self.logger = Logger.get_instance(log_file=self.log_file, log_level=logging.DEBUG, file_logging=True, console_logging=False)

    def tearDown(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        Logger.instance = None  # Reset the Logger instance for the next test

    def test_logging_to_file(self):
        self.logger.log("Test message", level=logging.INFO)
        with open(self.log_file, 'r') as f:
            self.assertIn("INFO - Test message", f.read())

    def test_logging_with_different_levels(self):
        self.logger.log("Debug message", level=logging.DEBUG)
        self.logger.log("Warning message", level=logging.WARNING)
        with open(self.log_file, 'r') as f:
            log_content = f.read()
            self.assertIn("DEBUG - Debug message", log_content)
            self.assertIn("WARNING - Warning message", log_content)

    def test_logging_exception(self):
        try:
            raise ValueError("Test exception")
        except Exception as e:
            with self.assertRaises(SystemExit):
                self.logger.log_exception(e)

        with open(self.log_file, 'r') as f:
            self.assertIn("ERROR - Exception occurred: Test exception", f.read())

    def test_disabled_logging(self):
        disabled_logger = Logger.get_instance(disabled=True)
        disabled_logger.log("This should not be logged", level=logging.INFO)
        self.assertFalse(os.path.exists(self.log_file))

    def test_console_logging_only(self):
        console_logger = Logger.get_instance(log_file=None, console_logging=True, file_logging=False)
        console_logger.log("Console only message", level=logging.INFO)
        self.assertFalse(os.path.exists(self.log_file))  # No file should be created

if __name__ == '__main__':
    unittest.main()
