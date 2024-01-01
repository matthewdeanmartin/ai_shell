import glob
import os
import shutil


class BackupRestore:
    @classmethod
    def revert_to_latest_backup(cls, file_name: str) -> str:
        """
        Revert the file to the most recent backup.

        Args:
            file_name (str): The name of the file to revert.

        Returns:
            str: A success message indicating the revert operation.

        Raises:
            ValueError: If no backup is found or other errors occur.
        """
        file_path = file_name
        backup_files = sorted(glob.glob(f"{file_path}.*.bak"), reverse=True)
        if not backup_files:
            raise ValueError(f"No backups found for {file_name}.")

        latest_backup = backup_files[0]
        bad_file_path = f"{file_path}.bad"

        try:
            if os.path.exists(file_path):
                os.rename(file_path, bad_file_path)
            os.rename(latest_backup, file_path)
            return f"Reverted {file_name} to latest backup."
        except Exception as e:
            raise ValueError(f"An error occurred during revert: {e}") from e

    @classmethod
    def backup_file(cls, file_name: str) -> str:
        """
        Create a backup of the file before overwriting it.

        Args:
            file_name (str): The name of the file to backup.

        Returns:
            str: A success message with the backup file path.

        Raises:
            ValueError: If the file does not exist or other errors occur.
        """
        file_path = file_name
        if not os.path.exists(file_name):
            raise ValueError(f"The file {file_name} does not exist.")

        # Find existing backups
        backup_files = sorted(glob.glob(f"{file_path}.*.bak"))
        backup_number = len(backup_files) + 1
        backup_file_path = f"{file_path}.{backup_number}.bak"

        try:
            shutil.copyfile(file_path, backup_file_path)
            return f"Backup created successfully at {backup_file_path}"
        except Exception as e:
            raise ValueError(f"An error occurred during backup: {e}") from e
