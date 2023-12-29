"""
AI Optimized version of find, but much simpler.

The bot confuses name with wildcard search.
"""
import fnmatch
import logging
import os
import re
from io import StringIO
from typing import Optional

from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log
from ai_shell.utils.read_fs import is_file_in_root_folder, remove_root_folder

logger = logging.getLogger(__name__)


class FindTool:
    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the FindTool class.

        Args:
            root_folder (str): The root folder path for file operations.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder
        self.config = config
        self.auto_cat = config.get_flag("auto_cat")

    @log()
    def find_files(
        self,
        name: Optional[str] = None,
        regex: Optional[str] = None,
        file_type: Optional[str] = None,
        size: Optional[str] = None,
    ) -> list[str]:
        """
        Recursively search for files or directories matching given criteria in a directory and its subdirectories.

        Args:
            name (Optional[str]): The exact name to match filenames against.
            regex (Optional[str]): The regex pattern to match filenames against.
            file_type (Optional[str]): The type to filter ('file' or 'directory').
            size (Optional[str]): The size to filter files by, e.g., '+100' for files larger than 100 bytes.

        Returns:
            list[str]: A list of paths to files or directories that match the criteria.
        """
        logger.info(f"find --name {name} --regex {regex} --type {file_type} --size {size}")
        matching_files = []
        for root, dirs, files in os.walk(self.root_folder):
            # Combine files and directories for type filtering
            combined = files
            if file_type == "directory":
                combined += dirs

            for entry in combined:
                full_path = os.path.join(root, entry)
                # TODO: handle this differently
                if os.path.dirname(full_path) != "__pycache__":
                    if is_file_in_root_folder(full_path, self.root_folder):
                        short_path = remove_root_folder(full_path, self.root_folder)
                        # Check for name, regex, and size match
                        if (name and fnmatch.fnmatch(entry, name)) or name is None:
                            if self._match_type_and_size(full_path, file_type, size):
                                matching_files.append(short_path)
                        elif regex and re.search(regex, entry):
                            if self._match_type_and_size(full_path, file_type, size):
                                matching_files.append(short_path)

        return list(sorted(matching_files))

    def _match_type_and_size(self, path: str, file_type: Optional[str], size: Optional[str]) -> bool:
        """
        Check if a file/directory matches the specified type and size criteria.

        Args:
            path (str): The path to the file/directory.
            file_type (Optional[str]): The type to filter ('file' or 'directory').
            size (Optional[str]): The size to filter files by.

        Returns:
            bool: True if the file/directory matches the criteria, False otherwise.
        """
        if file_type:
            if file_type == "file" and not os.path.isfile(path):
                return False
            if file_type == "directory" and not os.path.isdir(path):
                return False

        if size:
            size_prefix = size[0]
            size_value = int(size[1:])
            file_size = os.path.getsize(path)

            if size_prefix == "+" and file_size <= size_value:
                return False
            if size_prefix == "-" and file_size >= size_value:
                return False
        return True

    @log()
    def find_files_markdown(
        self,
        name: Optional[str] = None,
        regex: Optional[str] = None,
        file_type: Optional[str] = None,
        size: Optional[str] = None,
    ) -> str:
        """
        Recursively search for files or directories matching given criteria in a directory and its subdirectories.

        Args:
            name (Optional[str]): The exact name to match filenames against.
            regex (Optional[str]): The regex pattern to match filenames against.
            file_type (Optional[str]): The type to filter ('file' or 'directory').
            size (Optional[str]): The size to filter files by, e.g., '+100' for files larger than 100 bytes.

        Returns:
            str: Markdown of paths to files or directories that match the criteria.
        """
        output = StringIO()
        results = self.find_files(name, regex, file_type, size)
        for item in results:
            output.write(item)
            output.write("\n")
        output.seek(0)
        return output.read()
