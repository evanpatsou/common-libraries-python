import logging
import traceback
import sys
from typing import Optional

class Logger:
    """A singleton class for logging messages with different levels.

    The log messages can be written to both console and file, with the ability to disable either.
    There are 3 levels of log messages: INFO, WARNING, DEBUG. The format of the log message is 
    'current date and time [log level] log message'. The class also has an option to include a 
    progress bar in the log message and to log an exit message with the trace tree of an error.

    Attributes:
        instance (Logger): The singleton instance of the class.
        disabled (bool): Whether logging is enabled or not.
        logger (logging.Logger): The underlying logger object from the logging library.
    """
    instance = None  # type: Optional[Logger]

    @classmethod
    def get_instance(cls, log_file: Optional[str] = None, log_level: int = logging.DEBUG, 
                     file_format: Optional[str] = None, console_format: Optional[str] = None, 
                     disabled: bool = False, file_logging: bool = True, console_logging: bool = True) -> 'Logger':
        """Get the singleton instance of the class.

        Args:
            log_file (Optional[str]): The file path to log messages to. Defaults to None.
            log_level (int): The log level to log messages of that level or higher. Defaults to logging.DEBUG.
            file_format (Optional[str]): The format of log messages in the log file. Defaults to None.
            console_format (Optional[str]): The format of log messages in the console. Defaults to None.
            disabled (bool): Whether logging is enabled or not. Defaults to False.
            file_logging (bool): Whether to enable logging to a file. Defaults to True.
            console_logging (bool): Whether to enable logging to the console. Defaults to True.

        Returns:
            Logger: The singleton instance of the class.
        """
        if cls.instance is None:
            cls.instance = Logger(log_file, log_level, file_format, console_format, disabled, file_logging, console_logging)
        return cls.instance

    def __init__(self, log_file: Optional[str] = None, log_level: int = logging.DEBUG, 
                 file_format: Optional[str] = None, console_format: Optional[str] = None, 
                 disabled: bool = False, file_logging: bool = True, console_logging: bool = True):
        """Initialize the logger.

        Args:
            log_file (Optional[str]): The file path to log messages to. Defaults to None.
            log_level (int): The log level to log messages of that level or higher. Defaults to logging.DEBUG.
            file_format (Optional[str]): The format of log messages in the log file. Defaults to None.
            console_format (Optional[str]): The format of log messages in the console. Defaults to None.
            disabled (bool): Whether logging is enabled or not. Defaults to False.
            file_logging (bool): Whether to enable logging to a file. Defaults to True.
            console_logging (bool): Whether to enable logging to the console. Defaults to True.
        """
        self.disabled = disabled
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        
        if self.disabled:
            return
        
        if file_logging:
            self._init_file_handler(log_file, log_level, file_format)
        if console_logging:
            self._init_console_handler(log_level, console_format)

    def _init_file_handler(self, log_file: str, log_level: int, file_format: Optional[str]):
        """Initialize the file handler for the logger."""
        if log_file is not None:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_format = file_format or '%(asctime)s [%(levelname)s] %(message)s'
            file_formatter = logging.Formatter(file_format, datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

    def _init_console_handler(self, log_level: int, console_format: Optional[str]):
        """Initialize the console handler for the logger."""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_format = console_format or '%(asctime)s [%(levelname)s] %(message)s'
        console_formatter = logging.Formatter(console_format, datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def log(self, message: str, level: int = logging.INFO, progress_bar: Optional[int] = None):
        """Log a message with a given level.

        Args:
            message (str): The log message.
            level (int): The level of the log message. Defaults to logging.INFO.
            progress_bar (Optional[int]): The progress bar as a percentage. Defaults to None.
        """
        if self.disabled:
            return

        progress_bar_str = ''
        if progress_bar is not None:
            progress_bar_str = f' Progress: {progress_bar}%'
        
        self.logger.log(level, f'{datetime.datetime.now()} [%(levelname)s] {message}{progress_bar_str}')

    def log_exception(self, exc: Exception, level: int = logging.ERROR, exit_code: int = 1):
        """Log an exception with its trace tree and exit the program.

        Args:
            exc (Exception): The exception to log.
            level (int): The logging level for this message. Defaults to logging.ERROR.
            exit_code (int): The exit code to use when exiting the program. Defaults to 1.
        """
        if self.disabled:
            return

        # Extracting the stack trace and logging it
        exc_trace = traceback.format_exc()
        self.logger.log(level, f"Exception occurred: {exc}\nTraceback:\n{exc_trace}")

        # Exit the program
        sys.exit(exit_code)
