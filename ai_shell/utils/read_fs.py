"""
Grab bag of functions for file system.
"""

import glob
import logging
import math
import os
import re
from collections.abc import Generator
from contextlib import contextmanager
from itertools import islice
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


def sanitize_path(file_path: str) -> str:
    """Attempt to prevent parent directory traversal attacks by removing any leading '..' or '../' from the path.

    Args:
        file_path (str): The path to sanitize.

    Returns:
        str: The sanitized path.

    Examples:
        >>> sanitize_path("../foo/bar")
        'foo/bar'
        >>> sanitize_path("../../foo/bar")
        'foo/bar'
    """
    # Pattern to match sequences like '.', '..', '../', '..\', and so on at the beginning of the path
    pattern = r"^(?:\.\.?[\\/])*"
    sanitized_path = re.sub(pattern, "", file_path)
    return sanitized_path


def safe_glob(match_patten: str, root_dir: str):
    """Safely check for anything that doesn't break out of the root_dir"""
    match_patten = sanitize_path(match_patten)
    # dir_fd=None, recursive=False, include_hidden=False
    for result in glob.glob(
        match_patten,
        root_dir=root_dir,
    ):
        is_safe = is_file_in_root_folder(result, root_dir)
        if not is_safe:
            logger.warning(f"File {result} is not in root folder {root_dir}")
            continue

        yield result


def is_file_in_root_folder(file_path: str, root_folder: str) -> bool:
    """
    Check if a file could be in a given root folder or its subfolders.

    Args:
        file_path (str): The path to the file. It does not mean it exists!
        root_folder (str): The root folder path.

    Returns:
        bool: True if the file is in the root folder, False otherwise.

    Examples:
        >>> is_file_in_root_folder("foo/bar", ".")
        True
    """
    if "*" in root_folder or "?" in root_folder:
        raise ValueError("Root folder cannot contain wildcards")

    # Normalize paths to create absolute paths
    if not os.path.isabs(file_path):
        file_path = root_folder + "/" + file_path
    absolute_file_path = os.path.abspath(file_path)

    absolute_root_folder = os.path.abspath(root_folder)

    # Use os.path.commonpath to check if the root folder is a prefix of the file path
    common_path = os.path.commonpath([absolute_file_path, absolute_root_folder])
    # This won't work on linux, but on Windows I'm getting e: and E:!
    is_same = common_path.lower() == absolute_root_folder.lower()

    if not is_same:
        logger.warning(f"File {absolute_file_path} is not in root folder {absolute_root_folder}")
    return is_same


def tree(dir_path: Union[str, Path], level: int = -1, limit_to_directories: bool = False, length_limit: int = 1000):
    """Given a directory Path object print a visual tree structure
    Credits: https://stackoverflow.com/a/59109706/33264
    """
    space = "    "
    branch = "│   "
    tee = "├── "
    last = "└── "

    if isinstance(dir_path, str):
        dir_path = Path(dir_path)  # accept string coerceable to Path
    files = 0
    directories = 0

    result = ""

    def inner(dir_path: Path, prefix: str = "", level: int = -1):
        nonlocal files, directories
        if not level:
            return  # 0, stop iterating
        if limit_to_directories:
            contents = sorted(d for d in dir_path.iterdir() if d.is_dir())
        else:
            contents = sorted(_ for _ in dir_path.iterdir() if "__pycache__" not in str(_))
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents, strict=False):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space
                yield from inner(path, prefix=prefix + extension, level=level - 1)
            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1

    result += dir_path.name + "\n"
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        result += line + "\n"
    if next(iterator, None):
        result += f"... length_limit, {length_limit}, reached, counted:" + "\n"
    result += f"\n{directories} directories" + (f", {files} files" if files else "") + "\n"
    return result


# Flag to indicate if the context manager is currently active
_is_in_context = False


@contextmanager
def temporary_change_dir(new_dir: str) -> Generator[None, None, None]:
    """Context manager to temporarily change the current working directory.

    Args:
        new_dir (str): The new directory path.
    """
    # pylint:disable=global-statement
    global _is_in_context

    # Check if the context manager is already active
    if _is_in_context:
        raise RuntimeError("temporary_change_dir is already in use")

    if ".." in new_dir:
        raise ValueError("Cannot use .. in new_dir")

    _is_in_context = True
    original_dir = os.getcwd()
    new_dir = os.path.abspath(new_dir)

    if os.path.isfile(new_dir):
        new_dir = os.path.dirname(new_dir)

    # Check if the absolute paths are the same
    if original_dir != new_dir:
        os.chdir(new_dir)
        try:
            yield
        finally:
            os.chdir(original_dir)
            _is_in_context = False
    else:
        _is_in_context = False
        yield


def is_in_root_now(root_folder: str) -> bool:
    """
    Check if the provided path is an absolute path and if it's the same as the current working directory.

    Args:
    root_folder (str): The directory path to check.

    Returns:
    bool: True if `root_folder` is an absolute path and is the same as the current working directory, False otherwise.
    """
    root_folder = str(Path(".").resolve())
    # Check if the path is absolute
    if os.path.isfile(root_folder):
        root_folder = os.path.dirname(root_folder)

    is_absolute = os.path.isabs(root_folder)

    # Get the absolute path of the root_folder and the current working directory
    absolute_root_folder = os.path.abspath(root_folder)
    current_working_dir = os.getcwd()

    # Check if the absolute path of root_folder is the same as the current working directory
    is_same_as_pwd = absolute_root_folder == current_working_dir

    return is_absolute and is_same_as_pwd


def remove_root_folder(file_path: str, root_folder: str) -> str:
    """Removing root folder from path

    Args:
        file_path (str): The path to the file.
        root_folder (str): The root folder path. It must exist for this to succeed.

    Returns:
        str: The relative path of the file.
    """
    if not is_in_root_now(root_folder):
        raise ValueError(f"Root folder ({root_folder}) must be the current working directory, current {os.getcwd()}")
    # with temporary_change_dir(root_folder):
    root = Path(".").resolve()
    file = Path(file_path)

    # Handling the case where file_path is the same as root_folder
    if file.resolve() == root:
        return "."

    # Handling relative paths
    file = root / file if not file.is_absolute() else file
    file = file.resolve()

    if root in file.parents:
        return str(file.relative_to(root)).replace("\\", "/")
    raise ValueError("File path is not under the root folder")


def human_readable_size(size_in_bytes: int) -> str:
    """Converts a size in bytes to a human-readable format (e.g., KB, MB, GB).

    Args:
        size_in_bytes (int): The size in bytes.

    Returns:
        str: The size in human-readable format.

    Examples:
        >>> human_readable_size(0)
        '0 Bytes'
        >>> human_readable_size(1024)
        '1.0 KB'
        >>> human_readable_size(1024**2)
        '1.0 MB'
        >>> human_readable_size(1024**3)
        '1.0 GB'
        >>> human_readable_size(1024**4)
        '1.0 TB'
        >>> human_readable_size(1024**5)
        '1.0 PB'
        >>> human_readable_size(1024**6)
        '1.0 EB'
        >>> human_readable_size(1024**7)
        '1.0 ZB'
        >>> human_readable_size(1024**8)
        '1.0 YB'
    """
    # Define the units and their corresponding power of 1024
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    power = 1024

    # Calculate the logarithmic unit of the size
    if size_in_bytes > 0:
        unit = int(min((len(units) - 1), int(math.log(size_in_bytes, power))))
    else:
        unit = 0

    # Format the size with the appropriate unit
    if size_in_bytes > 0:
        readable_size = round(size_in_bytes / (power**unit), 2)
        return f"{readable_size} {units[unit]}"
    return "0 Bytes"


if __name__ == "__main__":
    # print(tree("../"))
    with temporary_change_dir("src"):
        with temporary_change_dir("src"):
            print("ok")
