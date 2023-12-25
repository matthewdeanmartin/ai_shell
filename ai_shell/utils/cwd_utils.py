"""Utilities for working with the current working directory."""

import os
from contextlib import contextmanager
from typing import Iterator, Never


@contextmanager
def change_directory(new_path: str) -> Iterator[Never]:
    """Change the current working directory to a new path.

    Args:
        new_path (str): The new path to change to.
    """
    original_directory = os.getcwd()
    try:
        os.chdir(new_path)
        yield
    finally:
        os.chdir(original_directory)
