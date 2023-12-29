"""
Optimized for AI version of sed. For file editing.

However, the bot keeps trying to use features of real sed that this tool doesn't support.
"""
import re

from ai_shell.cat_tool import CatTool
from ai_shell.pyutils.validate import is_python_file, is_valid_python_source
from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log
from ai_shell.utils.read_fs import is_file_in_root_folder


class SedTool:
    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the SedTool class.

        Args:
            root_folder (str): The root folder path for file operations.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder
        self.config = config
        self.auto_cat = config.get_flag("auto_cat")

    @log()
    def sed(self, file_path: str, commands: list[str]) -> str:
        r"""
        Transform the contents of a file located at file_path as per the provided sed-like commands.

        Args:
            file_path (str): The path of the file to be transformed.
            commands (list[str]): A list of sed-like commands for text transformation.

        Returns:
            str: The transformed text from the file.

        Supported command syntax:
            - s/regex/replacement/flags: Regex substitution.
            - p: Print the current line.
            - a\text: Append text after the current line.
            - i\text: Insert text before the current line.
            - [number]c\text: Change the text of a specific line number.
            - [number]d: Delete a specific line number.

        Note: This function reads from a file and returns the transformed text. It does not modify the file in-place.
        """
        if not is_file_in_root_folder(file_path, self.root_folder):
            raise ValueError(f"File {file_path} is not in root folder {self.root_folder}.")

        with open(file_path, encoding="utf-8") as file:
            input_text = file.read()
        output_text = SedTool._process_sed(input_text, commands)
        if is_python_file(file_path):
            is_valid, error = is_valid_python_source(output_text)
            if not is_valid and error is not None:
                return f"Invalid Python source code. No changes made. {error.lineno} {error.msg} {error.text}"

        if input_text != output_text:
            with open(file_path, "w", encoding="utf-8") as output_file:
                output_file.write(output_text)

            if self.auto_cat:
                feedback = "Changes without exception, please verify by other means.\n"
                contents = CatTool(self.root_folder, self.config).cat_markdown([file_path])
                return f"Tool feedback: {feedback}\n\nCurrent file contents:\n\n{contents}"
            return "Changes without exception, please verify by other means."
        return "No changes made."

    @classmethod
    def _process_sed(cls, input_text: str, commands: list[str]) -> str:
        r"""
        Transform input_text as per the provided sed-like commands.

        Args:
            input_text (str): The input text to be transformed.
            commands (list[str]): A list of sed-like commands for text transformation.

        Returns:
            str: The transformed text.

        Supported command syntax:
            - s/regex/replacement/flags: Regex substitution.
            - a\text: Append text after the current line.
            - i\text: Insert text before the current line.
            - [number]c\text: Change the text of a specific line number.
            - [number]d: Delete a specific line number.

        Example:
            >>> SedTool._process_sed("Hello World\\nThis is a test", ["s/World/Universe/", "a\\Appended text"])
            'Hello Universe\\nThis is a test\nAppended text'
            >>> SedTool._process_sed("First Line\\nSecond Line", ["2d", "i\\Inserted at Start"])
            'Inserted at Start\nFirst Line\\nSecond Line'
        """
        if isinstance(commands, str):
            commands = [commands]

        # don't know how to fix the covariant/invariant typing issue here
        lines: list[str] = input_text.split("\n")

        for i in range(len(lines)):
            for command in commands:
                if command.startswith("s/") and re.match(r"s/.+/.*/", command):
                    # Regex substitution: s/regex/replacement/flags
                    parts = command[2:].rsplit("/", 2)
                    regex, replacement, flags = parts[0], parts[1], parts[2] if len(parts) > 2 else ""
                    count = 1 if "g" not in flags else 0  # replace all if 'g' is present
                    lines[i] = re.sub(regex, replacement, lines[i], count=count)
                elif command.startswith("a\\"):
                    # Append: a\text
                    append_text = command[2:]
                    lines[i] += "\n" + append_text
                elif re.match(r"\d+a\\", command):
                    # insert "a"fter the specified line.
                    target_line, change_text = command.split("a\\")
                    if i + 1 == int(target_line):
                        lines[i] = change_text
                elif command.startswith("i\\") and i == 0:
                    # Insert: i\text (only at the beginning of the text)
                    insert_text = command[2:]
                    lines[i] = insert_text + "\n" + lines[i]
                elif re.match(r"\d+c\\", command):
                    # Change specific line: [number]c\text
                    target_line, change_text = command.split("c\\")
                    if i + 1 == int(target_line):
                        lines[i] = change_text
                elif re.match(r"\d+d", command):
                    # Delete specific line: [number]d
                    delete_line = int(command[:-1])
                    if i + 1 == delete_line:
                        # None was a better deletion marker, but messes with mypy.
                        lines[i] = "None  # Mark for deletion"
                elif command == "p":
                    # print? No action?
                    pass
                else:
                    raise TypeError(
                        "Unknown command, expected prefix of s/ or a\\ or digit + c or digit + d for replace, append, change, or delete respectively"
                    )

        # Rebuild the output from modified lines, excluding deleted ones
        output = [line for line in lines if line is not None]

        return "\n".join(output)

    # # Rerun the regex substitution test with the corrected function
    # test_regex_substitution_corrected = lambda: simulate_sed_corrected(input_text, commands) == expected_output
    # test_regex_substitution_corrected()


if __name__ == "__main__":

    def run():
        """Example usage"""
        # input_text = "Hello World\nThis is a test\nAnother line"
        # commands = ["s/World/Universe/", "a\\Appended text", "i\\Inserted text", "2c\\Changed line", "3d"]
        input_text = """
        print("ho")
        # TODO: Implement ocean waves across the top line of screen. That is a line of emojis!
        print("yo")
        """
        # commands = ["/^# TODO: Implement ocean waves across the top line of screen. That is a line of emojis!/a\\print('\\U0001F30A' * self.width) # Unicode for the water wave emoji"]
        commands = [
            "23a\\\ndef generate_ocean_waves():\\\n    # This function will create an animated line of wave emojis across the top line of the screen.\\\n    wave_emoji = u'\\U0001F30A'\\\n    top_line = wave_emoji * 80\\\n    print(top_line)\\\n"
        ]
        result = SedTool._process_sed(input_text, commands)
        print(result)

    run()
