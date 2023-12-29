"""
AI optimized cut tool.

The real version makes for sense for creating sql-like chains of pipes. I don't support pipe-like behavior yet.
"""
import csv
import dataclasses
import io
import logging
from typing import Optional, Union

from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log
from ai_shell.utils.read_fs import is_file_in_root_folder

logger = logging.getLogger(__name__)


def parse_ranges(range_str: str) -> list[Union[int, tuple[int, Optional[int]]]]:
    """Parses a range string into a list of integers and integer tuples.

    Args:
        range_str: A string representing ranges and numbers, e.g., "1-5,10".

    Returns:
        A list where each element is either an integer or a tuple of two integers.
    """
    ranges: list[Union[int, tuple[int, Optional[int]]]] = []
    for part in range_str.split(","):
        if "-" in part:
            start_string, end_string = part.split("-")
            start = int(start_string) if start_string else 1  # Handle incomplete ranges like '-5'
            end = int(end_string) if end_string else None  # Handle incomplete ranges like '5-'
            ranges.append((start, end))
        else:
            ranges.append(int(part))
    return ranges


def is_in_ranges(index: int, ranges: list[Union[int, tuple[int, Optional[int]]]]) -> bool:
    """Checks if a given index is within the specified ranges.

    Args:
        index: The index to check.
        ranges: A list of integers and integer tuples representing ranges.

    Returns:
        True if the index is within any of the ranges, False otherwise.
    """
    for r in ranges:
        if isinstance(r, tuple):
            start, end = r
            if end is None:
                if index >= start:
                    return True
            elif start <= index <= end:
                return True
        elif index == r:
            return True
    return False


@dataclasses.dataclass
class CutTool:
    """
    Simulates `cut` cli tool.
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
    def cut_characters(self, file_path: str, character_ranges: str) -> str:
        """Reads a file and extracts characters based on specified ranges.

        Args:
            file_path: The name of the file to process.
            character_ranges: A string representing character ranges, e.g., "1-5,10".

        Returns:
            A string containing the selected characters from the file.
        """
        if not is_file_in_root_folder(file_path, self.root_folder):
            raise ValueError(f"File {file_path} is not in root folder {self.root_folder}.")
        ranges = parse_ranges(character_ranges)
        output = io.StringIO()

        with open(file_path, encoding="utf-8") as file:
            for line in file:
                for i, char in enumerate(line, start=1):
                    if is_in_ranges(i, ranges):
                        output.write(char)

                # Optionally add a newline character after each line
                output.write("\n")

        return output.getvalue()

    @log()
    def cut_fields(self, filename: str, field_ranges: str, delimiter: str = ",") -> str:
        """Reads a file and extracts fields based on specified ranges using the given delimiter.

        Args:
            filename: The name of the file to process.
            field_ranges: A string representing field ranges, e.g., "1-3,5".
            delimiter: A single character used as the field delimiter.

        Returns:
            A string containing the selected fields from the file.
        """
        if not is_file_in_root_folder(filename, self.root_folder):
            raise ValueError(f"File {filename} is not in root folder {self.root_folder}.")
        ranges = parse_ranges(field_ranges)
        output = io.StringIO()

        with open(filename, encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=delimiter)

            for row in reader:
                selected_fields = [field for i, field in enumerate(row, start=1) if is_in_ranges(i, ranges)]
                output.write(delimiter.join(selected_fields) + "\n")

        return output.getvalue()

    @log()
    def cut_fields_by_name(self, filename: str, field_names: list[str], delimiter: str = ",") -> str:
        """Reads a file and extracts fields based on specified field names using the given delimiter.

        Args:
            filename: The name of the file to process.
            field_names: A list of field names to extract.
            delimiter: A single character used as the field delimiter.

        Returns:
            A string containing the selected fields from the file.
        """
        if not is_file_in_root_folder(filename, self.root_folder):
            raise ValueError(f"File {filename} is not in root folder {self.root_folder}.")
        output = io.StringIO()

        with open(filename, encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            # field_indices = {field: i for i, field in enumerate(reader.fieldnames)}

            for row in reader:
                selected_fields = [row[field] for field in field_names if field in row]
                output.write(delimiter.join(selected_fields) + "\n")

        return output.getvalue()
