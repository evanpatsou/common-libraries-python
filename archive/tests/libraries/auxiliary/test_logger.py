import unittest
import logging
import tempfile
import os
import sys
from logger import Logger  # Assuming the Logger class is in logger.py

class TestLogger(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for logging
        fd, self.log_file_name = tempfile.mkstemp()
        os.close(fd)  # Close the file descriptor

        # Initialize Logger with the temporary file name
        self.logger = Logger.get_instance(log_file=self.log_file_name, log_level=logging.DEBUG, file_logging=True, console_logging=False)

    def tearDown(self):
        # Delete the temporary log file after testing
        if os.path.exists(self.log_file_name):
            os.remove(self.log_file_name)
        Logger.instance = None  # Reset the Logger instance for the next test

    def test_logging_to_file(self):
        test_message = "Test message"
        self.logger.log(test_message, level=logging.INFO)
        with open(self.log_file_name, 'r') as f:
            self.assertIn(test_message, f.read())

    def test_logging_with_different_levels(self):
        self.logger.log("Debug message", level=logging.DEBUG)
        self.logger.log("Warning message", level=logging.WARNING)
        with open(self.log_file_name, 'r') as f:
            log_content = f.read()
            self.assertIn("Debug message", log_content)
            self.assertIn("Warning message", log_content)

    def test_logging_exception(self):
        try:
            raise ValueError("Test exception")
        except Exception as e:
            with self.assertRaises(SystemExit):
                self.logger.log_exception(e)

        with open(self.log_file_name, 'r') as f:
            self.assertIn("Test exception", f.read())

    def test_disabled_logging(self):
        disabled_logger = Logger.get_instance(disabled=True)
        disabled_logger.log("This should not be logged", level=logging.INFO)
        self.assertFalse(os.path.exists(self.log_file_name))

    def test_console_logging_only(self):
        # Redirect stdout to capture console output
        original_stdout = sys.stdout
        sys.stdout = open(self.log_file_name, 'w')
        
        console_logger = Logger.get_instance(log_file=None, console_logging=True, file_logging=False)
        console_logger.log("Console only message", level=logging.INFO)
        
        sys.stdout.close()
        sys.stdout = original_stdout

        with open(self.log_file_name, 'r') as f:
            self.assertIn("Console only message", f.read())

        if os.path.exists(self.log_file_name):
            os.remove(self.log_file_name)  # Clean up the temporary console log file

if __name__ == '__main__':
    unittest.main()
