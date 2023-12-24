import os
from contextlib import contextmanager


@contextmanager
def change_directory(new_path):
    original_directory = os.getcwd()
    try:
        os.chdir(new_path)
        yield
    finally:
        os.chdir(original_directory)
