import unittest
import csv
import os
from tempfile import NamedTemporaryFile
from data.source.file.handlers.csv_file_handler import CSVFileHandler

class TestCSVFileHandler(unittest.TestCase):

    def test_read_csv_file(self):
        """Test reading data from a CSV file."""
        # Create a temporary CSV file with some data
        with NamedTemporaryFile(mode='w', delete=False, newline='', suffix='.csv') as temp_file:
            writer = csv.writer(temp_file)
            writer.writerow(['name', 'age'])
            writer.writerow(['Alice', '30'])
            writer.writerow(['Bob', '35'])
            temp_filename = temp_file.name

        # Read data from the temporary CSV file
        handler = CSVFileHandler(temp_filename)
        data = handler.read()

        # Clean up the temporary file
        os.remove(temp_filename)

        # Assertions
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], ['Alice', '30'])
        self.assertEqual(data[1], ['Bob', '35'])

    def test_save_csv_file(self):
        """Test saving data to a CSV file."""
        data_to_save = [['name', 'age'], ['Alice', '30'], ['Bob', '35']]

        # Create a temporary CSV file
        with NamedTemporaryFile(mode='w', delete=False, newline='', suffix='.csv') as temp_file:
            temp_filename = temp_file.name

        # Save data to the temporary CSV file
        handler = CSVFileHandler(temp_filename)
        handler.save(data_to_save)

        # Read back the data
        with open(temp_filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            data_read = [row for row in reader]

        # Clean up the temporary file
        os.remove(temp_filename)

        # Assertions
        self.assertEqual(data_read, data_to_save)

if __name__ == '__main__':
    unittest.main()
