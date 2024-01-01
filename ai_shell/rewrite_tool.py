"""
For short files with lots of edits, just let the bot rewrite the file.

TODO: set maximum file size for re-write, because it costs tokens to rewrite a large file.
"""
import difflib
import logging
import os
from pathlib import Path
from typing import Optional

from ai_shell.ai_logs.log_to_bash import log
from ai_shell.backup_restore import BackupRestore
from ai_shell.cat_tool import CatTool
from ai_shell.pyutils.validate import ValidateModule, ValidationMessageForBot, is_python_file
from ai_shell.utils.config_manager import Config
from ai_shell.utils.read_fs import is_file_in_root_folder, sanitize_path, tree

logger = logging.getLogger(__name__)


def file_similarity(file1_path: str, file2_lines: list[str]) -> tuple[float, int, int, int, int]:
    """
    Compares the contents of a file with a list of strings (lines) and calculates the similarity.

    This function reads the contents of the file specified by `file1_path` and compares it line by line with
    the contents provided in `file2_lines`. It calculates the proportion of unchanged lines and the counts of
    total, unchanged, added, and removed lines.

    Args:
        file1_path (str): The path to the first file to compare.
        file2_lines (list[str]): A list of strings, where each string represents a line from the second file.

    Returns:
        tuple[float, int, int, int, int]: A tuple containing:
            - unchanged_proportion (float): The proportion of lines that remained unchanged.
            - total_lines (int): The total number of lines in the first file.
            - unchanged (int): The number of lines that remained unchanged.
            - added (int): The number of lines that were added in the second file.
            - removed (int): The number of lines that were removed in the second file.
    """
    # Read the contents of the files
    with open(file1_path, encoding="utf-8") as file1:
        file1_lines = file1.readlines()

    # Use difflib to get differences
    d = difflib.Differ()
    diff = list(d.compare(file1_lines, file2_lines))

    # Count the number of unchanged, added, and removed lines
    total_lines = len(file1_lines)
    unchanged = sum(1 for line in diff if line.startswith("  "))
    added = sum(1 for line in diff if line.startswith("+ "))
    removed = sum(1 for line in diff if line.startswith("- "))

    # Calculate the proportion of unchanged content
    unchanged_proportion = unchanged / total_lines if total_lines > 0.0 else 0.0

    return unchanged_proportion, total_lines, unchanged, added, removed


# Example usage:
# unchanged, added, removed = file_similarity('file1.txt', 'file2.txt')
# print(f"Unchanged lines: {unchanged}, Added lines: {added}, Removed lines: {removed}")


class RewriteTool:
    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the RewriteTool class.

        Args:
            root_folder (str): The root folder path for file operations.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder
        self.config = config
        self.auto_cat = config.get_flag("auto_cat", True)
        self.python_module = config.get_value("python_module")
        self.only_add_text = config.get_flag("only_add_text", False)

    @log()
    def write_new_file(self, file_path: str, text: str) -> str:
        """
        Write a new file at file_path within the root_folder.

        Args:
            file_path (str): The relative path to the file to be written.
            text (str): The content to write into the file.

        Returns:
            str: A success message with the file path.

        Raises:
            ValueError: If the file already exists or if the file_path is outside the root_folder.
        """
        file_path = sanitize_path(file_path)
        # Don't prepend root folder, we will have already cd'd to it.
        full_path = file_path
        if not is_file_in_root_folder(full_path, self.root_folder):
            raise ValueError("File path must be within the root folder.")

        try:
            if os.path.exists(full_path):
                raise FileExistsError("File already exists.")

            with open(full_path, "w", encoding="utf-8") as file:
                file.write(text)

            validation = self._validate_code(full_path)

            if validation:
                os.remove(full_path)
                return f"File not written because of problems.\n{validation.message}"

            return f"File written to {full_path}"
        except FileExistsError as e:
            tree_text = tree(Path(os.getcwd()))
            markdown_content = f"# File {full_path} already exists. Here are all the files you can see\n\n{tree_text}"
            raise ValueError(
                str(e) + f" {markdown_content}\n Consider using rewrite_file method if you want to overwrite."
            ) from e

    @log()
    def rewrite_file(self, file_path: str, text: str) -> str:
        """
        Backup and rewrite an existing file at file_path within the root_folder.
        This will completely replace the contents of the file with the new text.

        Args:
            file_path (str): The relative path to the file to be rewritten.
            text (str): The new content to write into the file.

        Returns:
            str: A success message with the file path.

        Raises:
            ValueError: If the file does not exist or if the file_path is outside the root_folder.
        """
        if not text:
            raise TypeError("This would delete everything in the file. This is probably not what you want.")

        file_path = sanitize_path(file_path)

        # Don't prepend root folder, we will have already cd'd to it.
        full_path = file_path
        if not is_file_in_root_folder(full_path, self.root_folder):
            raise ValueError("File path must be within the root folder.")

        # not sure this is working right.
        _unchanged_proportion, initial, unchanged, added, removed = file_similarity(full_path, text.split("\n"))
        if self.only_add_text and removed > 0:
            raise TypeError("This would delete lines. Only add lines, do not remove them.")
        if self.only_add_text and len(text.split("\n")) < initial:
            raise TypeError("Line count decreased. Only add text, do not remove it.")
        # if 5 < initial <= removed:
        #     # concern is taking a large file, and deleting everything (ie. confusing full rewrite for an insert or edit)
        #     raise TypeError(
        #         "Removed lines is equal initial number of lines. "
        #         "When rewriting files, you have to re-write the previous lines, too."
        #     )
        # if unchanged > 0 and initial > 0 and added == 0 and removed == 0:
        #     raise TypeError(
        #         "Nothing changed, nothing was added or removed. "
        #         "When rewriting files, you have to re-write the whole file "
        #         "with lines changed, added or removed."
        #     )

        try:
            if not os.path.exists(full_path):
                raise FileNotFoundError("File does not exist, use ls tool to see what files there are.")

            BackupRestore.backup_file(full_path)

            with open(full_path, "w", encoding="utf-8") as file:
                file.write(text)

            validation = self._validate_code(full_path)

            if validation:
                BackupRestore.revert_to_latest_backup(full_path)
                return f"File not rewritten because of problems.\n{validation.message}"

            feedback = f"File rewritten to {full_path}"
            if self.auto_cat:
                feedback = "Changes made without exception, please verify by other means.\n"
                contents = CatTool(self.root_folder, self.config).cat_markdown([file_path])
                return f"Tool feedback: {feedback}\n\nCurrent file contents:\n\n{contents}"
            return feedback + ", please view to verify contents."
        except FileNotFoundError as e:
            raise FileNotFoundError(
                str(e) + " Consider using write_new_file method if you want to create a new file."
            ) from e

    def _validate_code(self, full_path: str) -> Optional[ValidationMessageForBot]:
        """
        Validate python

        Args:
            full_path (str): The path to the file to validate.

        Returns:
            Optional[ValidationMessageForBot]: A validation message if the file is invalid, otherwise None.
        """
        if not is_python_file(full_path):
            return None
        if not self.python_module:
            logger.warning("No python module set, skipping validation.")
            return None
        validator = ValidateModule(self.python_module)
        results = validator.validate()
        explanation = validator.explain_to_bot(results)
        if explanation.is_valid:
            return None
        return explanation


if __name__ == "__main__":
    RewriteTool("./", Config()).write_new_file("src\\\\dialog_2.md", "print('hello world')")
