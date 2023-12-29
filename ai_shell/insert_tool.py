"""
Text editor for simple text insertion at line or context.
"""
from typing import Union

from ai_shell.cat_tool import CatTool
from ai_shell.pyutils.validate import is_python_file, is_valid_python_source
from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log


class InsertTool:
    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the InsertTool class.

        Args:
            root_folder (str): The root folder path for file operations.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder
        self.config = config
        self.auto_cat = config.get_flag("auto_cat")

    @log()
    def insert_text_after_context(self, file_path: str, context: str, text_to_insert: str) -> str:
        """Inserts a given text immediately after a specified context in a file.

        This method opens the file, finds the line containing the specified context,
        and inserts the provided text immediately after this line. If the context
        matches multiple lines, it raises a ValueError due to ambiguity.

        Args:
            file_path (str): The path of the file in which the text is to be inserted.
            context (str): The context string to search for in the file. The text is
                           inserted after the line containing this context.
            text_to_insert (str): The text to insert into the file.

        Returns:
            str: A message for the bot with the result of the insert.

        Raises:
            ValueError: If the provided context matches multiple lines in the file.
        """
        if not file_path:
            raise TypeError("No file_path, please provide file_path for each request.")
        if not context:
            raise TypeError("No context, please context so I can find where to insert the text.")
        with open(file_path, encoding="utf-8") as file:
            lines = file.readlines()
        original_lines = list(lines)

        context_line_indices = [i for i, line in enumerate(lines) if context in line]

        # Check for ambiguity in the context match
        if len(context_line_indices) != 1:
            raise ValueError(
                "Ambiguous context: The provided context matches multiple lines. A context line the "
                "string or substring of the line just before your desired insertion point. It must "
                "uniquely identify a location. Either use a longer substring to match or switch to using"
                "the insert_text_after_multiline_context tool."
            )

        # Index of the line after the context line
        insert_index = context_line_indices[0] + 1

        # Insert the text
        lines.insert(insert_index, text_to_insert + "\n")

        return self._save_if_changed(file_path, original_lines, lines)

    @log()
    def insert_text_at_start_or_end(self, file_path: str, text_to_insert: str, position: str = "end") -> str:
        """Inserts text at the start or end of a file.

        Opens the file and inserts the specified text either at the beginning or the
        end of the file, based on the 'position' argument. If the position argument
        is neither 'start' nor 'end', it raises a ValueError.

        Args:
            file_path (str): The path of the file in which the text is to be inserted.
            text_to_insert (str): The text to insert into the file.
            position (str, optional): The position where the text should be inserted.
                                      Should be either 'start' or 'end'. Defaults to 'end'.

        Raises:
            ValueError: If the 'position' argument is not 'start' or 'end'.

        """
        if not file_path:
            raise TypeError("No file_path, please provide file_path for each request.")
        if not text_to_insert:
            raise TypeError("No text_to_insert, please provide so I have something to insert.")
        if position not in ("start", "end"):
            raise ValueError("position must be start or end, so I know where to insert text.")
        with open(file_path, encoding="utf-8") as file:
            lines = file.readlines()
        original_lines = list(lines)
        if position == "start":
            lines.insert(0, text_to_insert + "\n")
        elif position == "end":
            lines.append(text_to_insert + "\n")
        else:
            raise ValueError("Invalid position: choose 'start' or 'end'.")

        return self._save_if_changed(file_path, original_lines, lines)

    @log()
    def insert_text_after_multiline_context(self, file_path: str, context_lines: list[str], text_to_insert: str) -> str:
        """Inserts text immediately after a specified multiline context in a file.

        Opens the file and searches for a sequence of lines (context). Once the context
        is found, it inserts the specified text immediately after this context. If the
        context is not found, it raises a ValueError.

        Args:
            file_path (str): The path of the file in which the text is to be inserted.
            context_lines (list of str): A list of strings representing the multiline
                                         context to search for in the file.
            text_to_insert (str): The text to insert into the file after the context.

        Raises:
            ValueError: If the multiline context is not found in the file.

        """
        if not file_path:
            raise TypeError("No file_path, please provide file_path for each request.")
        if not context_lines:
            raise TypeError("No context_lines, please context lines so I can find where to insert the new lines.")
        with open(file_path, encoding="utf-8") as file:
            lines = file.readlines()

        try:
            ends_with_n = lines[:-1][0].endswith("\n")
        except IndexError:
            ends_with_n = False

        # this is going to make it hard to preserve whitespace.
        # Convert context_lines to a string for easier matching
        context_string = "".join([line + "\n" for line in context_lines]).rstrip("\n")

        # Convert file lines to a string
        file_string = "".join(lines)

        starts_at = file_string.find(context_string)
        if starts_at == -1:
            raise ValueError("Context not found in the file.")

        # Find the index where the context ends
        context_end_index = starts_at + len(context_string)

        # Split the file_string back into lines at the context end
        before_context = file_string[:context_end_index]
        after_context = file_string[context_end_index:]

        # Insert the new text
        new_file_string = before_context + "\n" + text_to_insert + "\n" + after_context.strip("\n")

        if ends_with_n:
            new_file_string += "\n"

        return self._save_if_changed(file_path, lines, new_file_string)

    def _save_if_changed(self, file_path: str, original_lines, new_file_string: Union[str, list[str]]) -> str:
        """
        Save the file if it has changed.

        Args:
            file_path: The path of the file to save.
            original_lines: The original file contents.
            new_file_string: The new file contents.

        Returns:
            A message for the bot with the result of the save.
        """
        if not new_file_string:
            raise TypeError("Something went wrong in insert and all text disappeared. Cancelling.")
        if isinstance(new_file_string, list):
            source = "\n".join(new_file_string)
        else:
            source = new_file_string
        if isinstance(new_file_string, str) and "\n".join(original_lines) == new_file_string:
            return (
                "File not changed this means the old file contents are the same as the new. This has nothing "
                "to do with file permissions."
            )
        if isinstance(new_file_string, list) and original_lines == new_file_string:
            return (
                "File not changed, this means the old file contents are the same as the new. This has nothing "
                "to do with file permissions."
            )
        if is_python_file(file_path):
            is_valid, error = is_valid_python_source(source)
            if not is_valid and error:
                return f"Invalid Python source code. No changes made. {error.lineno} {error.msg} {error.text}"
            if not is_valid:
                return f"Invalid Python source code. No changes made. {error}."

        # Write back to the file
        with open(file_path, "w", encoding="utf-8") as file:
            if isinstance(new_file_string, str):
                file.write(new_file_string)
            else:
                file.writelines(new_file_string)
        if self.auto_cat:
            feedback = "Insert completed and no exceptions thrown."
            contents = CatTool(self.root_folder, self.config).cat_markdown([file_path])
            return f"Tool feedback: {feedback}\n\nCurrent file contents:\n\n{contents}"
        return "Insert completed and no exceptions thrown. Please verify by other means."
