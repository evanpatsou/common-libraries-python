import unittest
import logging
import tempfile
import os
from logger import Logger  # Assuming the Logger class is in logger.py

class TestLogger(unittest.TestCase):

    def setUp(self):
        # Create a temporary file and then close and delete it to use its path
        fd, self.log_file_name = tempfile.mkstemp()
        os.close(fd)
        os.remove(self.log_file_name)

        # Initialize Logger with the temporary file path
        self.logger = Logger.get_instance(log_file=self.log_file_name, log_level=logging.DEBUG, file_logging=True, console_logging=False)

    def tearDown(self):
        # Reset the Logger instance for the next test
        Logger.instance = None

        # Attempt to delete the temporary log file after testing
        for _ in range(5):  # Retry mechanism
            try:
                if os.path.exists(self.log_file_name):
                    os.remove(self.log_file_name)
                break
            except PermissionError:
                time.sleep(1)  # Wait a bit and retry

    def read_log_content(self):
        with open(self.log_file_name, 'r') as f:
            return f.read()

    def test_logging_to_file(self):
        test_message = "Test message"
        self.logger.log(test_message, level=logging.INFO)
        log_content = self.read_log_content()
        self.assertIn(test_message, log_content)

    def test_logging_with_different_levels(self):
        self.logger.log("Debug message", level=logging.DEBUG)
        self.logger.log("Warning message", level=logging.WARNING)
        log_content = self.read_log_content()
        self.assertIn("Debug message", log_content)
        self.assertIn("Warning message", log_content)

    def test_logging_exception(self):
        try:
            raise ValueError("Test exception")
        except Exception as e:
            with self.assertRaises(SystemExit):
                self.logger.log_exception(e)

        log_content = self.read_log_content()
        self.assertIn("Test exception", log_content)

    def test_disabled_logging(self):
        disabled_logger = Logger.get_instance(disabled=True)
        disabled_logger.log("This should not be logged", level=logging.INFO)
        log_content = self.read_log_content()
        self.assertNotIn("This should not be logged", log_content)

    def test_console_logging_only(self):
        console_logger = Logger.get_instance(log_file=None, console_logging=True, file_logging=False)
        console_logger.log("Console only message", level=logging.INFO)
        # Not checking the console output as it's not feasible in unittest

if __name__ == '__main__':
    unittest.main()
