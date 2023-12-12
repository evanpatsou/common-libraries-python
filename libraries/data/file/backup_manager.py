import shutil
from pathlib import Path
from datetime import datetime

class BackupManager:
    """
    Handles the backup of files.

    This class is responsible for creating backups of files in an 'archive' folder
    within the file's directory, if the file exists.
    """

    def create_backup(self, file_path: str, raise_error_if_not_found: bool = False) -> None:
        """
        Creates a backup of the specified file in an 'archive' folder. Optionally,
        raises an error if the file does not exist.

        Args:
            file_path (str): The path of the file to backup.
            raise_error_if_not_found (bool): If True, raises FileNotFoundError when the file does not exist.

        Raises:
            FileNotFoundError: If raise_error_if_not_found is True and no file is found at file_path.
            IOError: If there is an error in creating the backup.
        """
        original_path = Path(file_path)

        if not original_path.exists():
            if raise_error_if_not_found:
                raise FileNotFoundError(f"No file found at {file_path}")
            else:
                return  # Exit the function if the file doesn't exist and raising an error is not required

        backup_path = self._get_backup_path(original_path)
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.copy2(file_path, backup_path)
        except IOError as e:
            raise IOError(f"Failed to create backup for {file_path}: {e}")

    def _get_backup_path(self, original_path: Path) -> Path:
        """
        Generates the backup path for a file within an 'archive' folder.

        Args:
            original_path (Path): The original path of the file.

        Returns:
            Path: The path where the backup will be stored.
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_folder = original_path.parent / "archive"
        backup_filename = f"{original_path.stem}_{timestamp}{original_path.suffix}"
        return backup_folder / backup_filename
