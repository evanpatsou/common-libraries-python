import unittest
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from data.backup.backup_manager import BackupManager

class TestBackupManager(unittest.TestCase):

    def setUp(self):
        """Set up a BackupManager instance for testing."""
        self.backup_manager = BackupManager()

    def test_backup_creation(self):
        """Test creating a backup of an existing file."""
        # Create a temporary file
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b'Test data')
            temp_filename = temp_file.name

        # Create a backup
        self.backup_manager.create_backup(temp_filename)

        # Check if backup file exists
        backup_path = Path(temp_filename).parent / "archive"
        backup_files = list(backup_path.glob('*.tmp'))
        self.assertEqual(len(backup_files), 1)

        # Clean up
        os.remove(temp_filename)
        os.remove(backup_files[0])

    def test_backup_non_existent_file(self):
        """Test backup creation behavior with a non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.backup_manager.create_backup('non_existent_file.tmp', raise_error_if_not_found=True)

        # Test without raising an error
        self.assertIsNone(self.backup_manager.create_backup('non_existent_file.tmp'))

if __name__ == '__main__':
    unittest.main()
