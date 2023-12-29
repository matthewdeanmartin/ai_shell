"""
Cat optimized for AI prompts.
"""
import logging
import os.path
from collections.abc import Generator
from io import StringIO
from typing import IO

from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log
from ai_shell.utils.read_fs import is_file_in_root_folder, safe_glob
from ai_shell.utils.type_repair import convert_to_list

logger = logging.getLogger(__name__)


class CatTool:
    """
    Simulates `cat` cli tool.
    """

    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the CatTool class.

        Args:
            root_folder (str): The root folder path for file operations.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder
        self.config = config

    @log()
    def cat_markdown(
        self,
        file_paths: list[str],
        number_lines: bool = True,
        squeeze_blank: bool = False,
    ) -> str:
        """
        Concatenates the content of given file paths and formats them as markdown.

        Args:
            file_paths (list[str]): List of file paths to concatenate.
            number_lines (bool): If True, number all output lines.
            squeeze_blank (bool): If True, consecutive blank lines are squeezed to one.

        Returns:
            str: The concatenated and formatted content as a string.
        """
        output = StringIO()
        for line in self.cat(file_paths, number_lines, squeeze_blank):
            output.write(line)
            # output.write("\n")
        output.seek(0)
        return output.read()

    @log()
    def cat(
        self,
        file_paths: list[str],
        number_lines: bool = True,
        squeeze_blank: bool = False,
    ) -> Generator[str, None, None]:
        """
        Mimics the basic functionalities of the 'cat' command in Unix.

        Args:
            file_paths (list[str]): A list of file paths to concatenate.
            number_lines (bool): If True, number all output lines.
            squeeze_blank (bool): If True, consecutive blank lines are squeezed to one.

        Returns:
            Generator[str, None, None]

        Yields:
            str: Each line of the concatenated files.
        """
        file_paths = convert_to_list(file_paths)
        for location, file_path in enumerate(file_paths):
            if file_path.startswith("./"):
                file_paths[location] = file_path[2:]

        logger.info(f"cat --file_paths {file_paths} " f"--number_lines {number_lines} --squeeze_blank {squeeze_blank}")
        for file_path in file_paths:
            if not is_file_in_root_folder(file_path, self.root_folder):
                raise TypeError("No parent folder traversals allowed")

        line_number = 1
        for glob_pattern in file_paths:
            for file_path in safe_glob(glob_pattern, self.root_folder):
                if not os.path.isabs(file_path):
                    file_path = self.root_folder + "/" + file_path
                try:
                    with open(file_path, "rb") as file:
                        for line in self._process_cat_file(file, line_number, number_lines, squeeze_blank):
                            yield line
                            line_number += 1
                except PermissionError:
                    logger.warning(f"Permission denied: {file_path}, suppressing from output.")

    def _process_cat_file(
        self,
        file: IO[bytes],
        line_number: int,
        number_lines: bool,
        squeeze_blank: bool,
    ) -> Generator[str, None, None]:
        """
        Processes a file for concatenation, applying the specified formatting.

        Args:
            file: The file object to process.
            line_number (int): Current line number for numbering lines.
            number_lines (bool): If True, number all output lines.
            squeeze_blank (bool): If True, consecutive blank lines are squeezed to one.

        Returns:
            Generator[str, None, None]: A generator of processed lines.

        Yields:
            str: Each processed line of the file.
        """
        was_blank = False
        for byte_lines in file:
            # if isinstance(byte_lines, bytes):
            line = byte_lines.decode("utf-8")  # Decode bytes to string

            # Use StringIO for memory-efficient line processing
            with StringIO() as line_buffer:
                # Normalize line endings to \n
                line = line.replace("\r\n", "\n")
                line_buffer.write(line)

                if squeeze_blank and was_blank and line.strip() == "":
                    continue  # Skip consecutive blank lines

                was_blank = line.strip() == ""

                if number_lines:
                    line_buffer.seek(0)
                    line = f"{line_number}\t{line_buffer.read()}"
                    line_number += 1
                else:
                    line = line_buffer.getvalue()

                yield line


if __name__ == "__main__":
    tool = CatTool(root_folder="./..", config=Config(".."))

    for thing in tool.cat(file_paths=["*.py"]):
        print(thing, end="")
