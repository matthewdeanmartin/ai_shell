"""
Optimized for AI version of sed. For file editing.

However, the bot keeps trying to use features of real sed that this tool doesn't support.
"""

import logging
import re
from typing import Optional

from ai_shell.ai_logs.log_to_bash import log
from ai_shell.backup_restore import BackupRestore
from ai_shell.cat_tool import CatTool
from ai_shell.pyutils.validate import ValidateModule, ValidationMessageForBot, is_python_file
from ai_shell.utils.config_manager import Config

logger = logging.getLogger(__name__)


class ReplaceTool:
    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the SedTool class.

        Args:
            root_folder (str): The root folder path for file operations.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder
        self.config = config
        self.auto_cat = config.get_flag("auto_cat", True)
        self.python_module = config.get_value("python_module")
        self.utf8_errors = config.get_value("utf8_errors", "surrogateescape")

    @log()
    def replace_line_by_line(
        self, file_path: str, old_text: str, new_text: str, line_start: int = 0, line_end: int = -1
    ) -> str:
        """Replaces occurrences of a specified text with new text in a range of lines in a file.

        Opens the file and replaces occurrences of 'old_text' with 'new_text' within the specified
        line range. If 'line_end' is -1, it defaults to the end of the file. Returns a message
        indicating whether changes were successfully applied or not.

        Args:
            file_path (str): The path to the file.
            old_text (str): The text to be replaced.
            new_text (str): The new text to replace the old text.
            line_start (int, optional): The starting line number (0-indexed) for the replacement.
                                        Defaults to 0.
            line_end (int, optional): The ending line number (0-indexed) for the replacement.
                                      If -1, it goes to the end of the file. Defaults to -1.

        Returns:
            str: A message indicating the success of the operation.

        Raises:
            TypeError: If file_path or old_text is None, or if no lines are left after replacement.
        """
        if not file_path:
            raise TypeError("No file_path, please provide file_path for each request.")
        if not old_text:
            raise TypeError("No old_text, please context so I can find the text to replace.")
        with open(file_path, encoding="utf-8", errors=self.utf8_errors) as file:
            input_text = file.read()
        lines = []
        input_lines = input_text.splitlines()
        if line_end == -1:
            line_end = len(input_lines)
        for line_no, line in enumerate(input_lines):
            if line_start <= line_no < line_end and old_text in line:
                line = line.replace(old_text, new_text)
            lines.append(line)
        if not lines:
            raise TypeError("Nothing left after replace, something went wrong, cancelling.")
        final = "\n".join(lines)
        return self._save_if_changed(file_path, final, input_text)

    @log()
    def replace_all(self, file_path: str, old_text: str, new_text: str) -> str:
        """Replaces all occurrences of a specified text with new text in a file.

        Opens the file and replaces all occurrences of 'old_text' with 'new_text'. Returns a
        message indicating whether changes were successfully applied or not.

        Args:
            file_path (str): The path to the file.
            old_text (str): The text to be replaced.
            new_text (str): The new text to replace the old text.

        Returns:
            str: A message indicating the success of the operation.

        Raises:
            TypeError: If file_path or old_text is None.
        """
        if new_text is None:
            new_text = ""
        if not file_path:
            raise TypeError("No file_path, please provide file_path for each request.")
        if not old_text:
            raise TypeError("No old_text, please context so I can find the text to replace.")
        with open(file_path, encoding="utf-8", errors=self.utf8_errors) as file:
            input_text = file.read()
        final = input_text.replace(old_text, new_text)
        return self._save_if_changed(file_path, final, input_text)

    @log()
    def replace_with_regex(self, file_path: str, regex_match_expression: str, replacement: str) -> str:
        """Replaces text in a file based on a regular expression match.

        Opens the file and replaces text that matches the regular expression 'regex_match_expression'
        with the 'replacement' text. Returns a message indicating whether changes were successfully
        applied or not.

        Args:
            file_path (str): The path to the file.
            regex_match_expression (str): The regular expression pattern to match.
            replacement (str): The text to replace the matched pattern.

        Returns:
            str: A message indicating the success of the operation.

        Raises:
            TypeError: If file_path or regex_match_expression is None.
        """
        if not file_path:
            raise TypeError("No file_path, please provide file_path for each request.")
        if not regex_match_expression:
            raise TypeError("No regex_match_expression, please context so I can find the text to replace.")
        with open(file_path, encoding="utf-8", errors=self.utf8_errors) as file:
            input_text = file.read()
        final = re.sub(regex_match_expression, replacement, input_text)
        return self._save_if_changed(file_path, final, input_text)

    def _save_if_changed(self, file_path: str, final: str, input_text: str) -> str:
        """Saves the modified text to the file if changes have been made.

        Compares the original text with the modified text and writes the modified text
        to the file if there are changes. Returns a message indicating whether any changes
        were made.

        Args:
            file_path (str): The path to the file.
            final (str): The modified text.
            input_text (str): The original text.

        Returns:
            str: A message indicating whether changes were made or not.

        Raises:
            TypeError: If file_path is None.
        """
        if not final:
            raise TypeError("Something went wrong in replace and all text disappeared. Cancelling.")

        if input_text != final:
            BackupRestore.backup_file(file_path)
            with open(file_path, "w", encoding="utf-8", errors=self.utf8_errors) as output_file:
                output_file.write(final)

            validation = self._validate_code(file_path)

            if validation:
                BackupRestore.revert_to_latest_backup(file_path)
                return f"File not written because of problems.\n{validation.message}"

            if self.auto_cat:
                feedback = "Changes applied without exception, please verify by other means.\n"
                contents = CatTool(self.root_folder, self.config).cat_markdown([file_path])
                return f"Tool feedback: {feedback}\n\nCurrent file contents:\n\n{contents}"
            return "Changes applied without exception, please verify by other means."
        return (
            "No changes made, this means the old file contents are the same as the new. This has nothing "
            "to do with file permissions. Try again with a different match pattern."
        )

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
