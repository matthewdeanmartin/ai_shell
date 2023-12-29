"""
Validate python by a variety of strategies.
"""
import ast
import hashlib
import os
from dataclasses import dataclass
from typing import Optional

import ai_shell.externals as externals
from ai_shell.externals.subprocess_utils import CommandResult


def hash_file(file_path: str) -> str:
    """Compute the hash of a single file."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        buf = file.read(65536)  # Read the file in chunks
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(65536)
    return hasher.hexdigest()


def hash_directory(directory_path: str) -> dict[str, str]:
    """Recursively hash all files in a directory."""
    hashes = {}
    for root, _dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            hashes[file_path] = hash_file(file_path)
    return hashes


def is_valid_python_file(file_name: str) -> bool:
    """
    Check if a given file is a valid Python file.

    Args:
        file_name (str): The file name or path to check.

    Returns:
        bool: True if the file is a valid Python file, False otherwise.
    """
    with open(file_name, encoding="utf-8") as file:
        contents = file.read()
    is_valid, error = is_valid_python_source(contents)
    return is_valid


def is_valid_python_source(text: str) -> tuple[bool, Optional[SyntaxError]]:
    """
    Check if a given string is valid Python source code.

    Args:
        text (str): The Python source code to check.

    Returns:
        bool: True if the source code is valid, False otherwise.
        SyntaxError: The SyntaxError that was raised, if any.
    """
    try:
        ast.parse(text)
        # or compile(contents, fname, 'exec', ast.PyCF_ONLY_AST)
        return True, None
    except SyntaxError as exception:
        return False, exception


def is_python_file(file: str) -> bool:
    """
    Check if a given file is a Python file.

    Args:
        file (str): The file name or path to check.

    Returns:
        bool: True if the file extension is .py, False otherwise.
    """
    return file.endswith(".py")


@dataclass
class ValidationMessageForBot:
    is_valid: bool
    message: str


class ValidateModule:
    def __init__(self, module_path: str):
        self.module_path = module_path
        self.initial_errors = self.validate(early_exit=False)
        self.initial_hash = hash_directory(module_path)

    def validate(self, early_exit: bool = True) -> list[CommandResult]:
        """Validate with black, pylint, mypy. Looking for fatal errors"""
        results_so_far: list[CommandResult] = []
        ruff_result = externals.invoke_ruff(self.module_path)
        if ruff_result.return_code == 1:
            results_so_far.append(ruff_result)
            if early_exit:
                return results_so_far

        black_result = externals.invoke_black(self.module_path)
        if black_result.return_code == 123:
            results_so_far.append(black_result)
            if early_exit:
                return results_so_far
        mypy_result = externals.invoke_mypy(self.module_path)
        if mypy_result.return_code == 2:
            results_so_far.append(black_result)
            if early_exit:
                return results_so_far
        pylint_result = externals.invoke_pylint(self.module_path, 1.0)
        if pylint_result.return_code in (1, 2):
            results_so_far.append(black_result)
            if early_exit:
                return results_so_far

        return results_so_far

    def explain_to_bot(self, current_errors: list[CommandResult]) -> ValidationMessageForBot:
        """Explain to the bot what happened."""
        current_hash = hash_directory(self.module_path)
        # Bot didn't do anything
        if self.initial_hash == current_hash and not current_errors:
            return ValidationMessageForBot(True, "No changes made to the module and the module is valid python.")

        # Bot didn't do anything but it's still broken
        if self.initial_hash == current_hash and current_errors:
            message = "No changes made to the module, but it is still invalid python.\n\n"
            message += "Current state is:\n"
            for result in current_errors:
                message += f"{result.to_markdown()}\n"
            return ValidationMessageForBot(False, message)

        # Bot fixed it
        if self.initial_errors and not current_errors:
            return ValidationMessageForBot(
                True, "The module was invalid python before editing, but now it is valid python."
            )

        # It was fine and bot broke it.
        if not self.initial_errors and current_errors:
            message = "The module was valid python before editing, but now it is invalid python.\n\n"
            message += "Current state is:\n"
            for result in current_errors:
                message += f"{result.to_markdown()}\n"
            return ValidationMessageForBot(False, message)

        # The code was a mess and still is
        if self.initial_errors and current_errors:
            message = "The module was invalid python before editing, and now it is still invalid python.\n\n"
            message += "Current state is:\n"
            for result in current_errors:
                message += f"{result.to_markdown()}\n"
            return ValidationMessageForBot(False, message)

        if not self.initial_errors and not current_errors:
            return ValidationMessageForBot(
                True, "The module was valid python before editing, and now it is still valid python."
            )

        raise ValueError("This should be unreachable.")


if __name__ == "__main__":
    # check file on init.
    v = ValidateModule("../../src/fish_tank/__main__.py")
    # Check file now
    # Explain if it got better/worse

    print(v.explain_to_bot(v.validate()))
