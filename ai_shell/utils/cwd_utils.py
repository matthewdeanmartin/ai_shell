"""Utilities for working with the current working directory."""

import os
from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def change_directory(new_path: str) -> Iterator[None]:
    """Change the current working directory to a new path.

    Args:
        new_path (str): The new path to change to.
    """
    original_directory = os.getcwd()
    try:
        os.chdir(new_path)
        yield None
    finally:
        os.chdir(original_directory)
