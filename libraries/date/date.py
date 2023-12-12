import datetime
import logging
from typing import List, Optional

class DateHandler:
    """
    A class for handling various date-related operations.

    Attributes:
        formats (List[str]): List of date formats supported for parsing.
        date (datetime.datetime): The current date held by the instance.

    Args:
        date (Optional[str]): A string representing a date. If provided, it will be parsed based on the supported formats.
        additional_formats (Optional[List[str]]): Additional date formats to be considered for parsing.

    Raises:
        ValueError: If the provided date string does not match any of the supported formats.
    """

    default_formats = ['%Y-%m-%d', '%Y%m%d', '%d-%m-%Y', '%d/%m/%Y', '%m-%d-%Y', '%m/%d/%Y']

    def __init__(self, date: Optional[str] = None, additional_formats: Optional[List[str]] = None):
        self.formats = self.default_formats + (additional_formats or [])
        self.date = self.parse(date) if date else datetime.datetime.now()
        logging.basicConfig(level=logging.INFO)

    def parse(self, date_str: str) -> datetime.datetime:
        """
        Parse a date string into a datetime object based on the supported formats.

        Args:
            date_str (str): The date string to parse.

        Returns:
            datetime.datetime: The parsed date.

        Raises:
            ValueError: If the date string does not match any of the supported formats.
        """
        for fmt in self.formats:
            try:
                return datetime.datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unsupported date format. Supported formats: {', '.join(self.formats)}")

    def __str__(self) -> str:
        return self.date.strftime('%Y-%m-%d')

    def update_date(self, new_date: str) -> None:
        """
        Update the internal date to a new date based on the supported formats.

        Args:
            new_date (str): The new date string to update.
        """
        self.date = self.parse(new_date)

    def add_days(self, days: int) -> None:
        """
        Add a number of days to the current date.

        Args:
            days (int): The number of days to add.
        """
        self.date += datetime.timedelta(days=days)

    def format_date(self, format_string: str) -> str:
        """
        Format the current date into a string based on the given format.

        Args:
            format_string (str): The format string to use for formatting the date.

        Returns:
            str: The formatted date string.
        """
        return self.date.strftime(format_string)

    def find_latest_friday(self) -> None:
        """
        Update the internal date to the most recent Friday.
        """
        days_behind = (self.date.weekday() - 4) % 7
        self.date -= datetime.timedelta(days=days_behind)

    def __eq__(self, other: 'DateHandler') -> bool:
        """
        Check if the current date is equal to the date of another DateHandler instance.

        Args:
            other (DateHandler): The other DateHandler instance to compare with.

        Returns:
            bool: True if the dates are equal, False otherwise.
        """
        return self.date == other.date

    def __lt__(self, other: 'DateHandler') -> bool:
        """
        Check if the current date is less than the date of another DateHandler instance.

        Args:
            other (DateHandler): The other DateHandler instance to compare with.

        Returns:
            bool: True if the current date is earlier, False otherwise.
        """
        return self.date < other.date

    def __le__(self, other: 'DateHandler') -> bool:
        """
        Check if the current date is less than or equal to the date of another DateHandler instance.

        Args:
            other (DateHandler): The other DateHandler instance to compare with.

        Returns:
            bool: True if the current date is earlier or equal, False otherwise.
        """
        return self.date <= other.date