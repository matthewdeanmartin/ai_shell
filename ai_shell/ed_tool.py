"""
Ed is a bad editor, but it is documented.

This
"""
import os
from typing import Any

from ed.buffer import Buffer

from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log
from ai_shell.utils.read_fs import sanitize_path


class EdTool:
    """A python version of ed."""

    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the EdTool class.

        Args:
            root_folder (str): The root folder path for file operations.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder if root_folder.endswith("/") else root_folder + "/"
        self.buffer = Buffer()
        self.config = config
        self.auto_cat = config.get_flag("auto_cat")

    @log()
    def ed(self, script: str, file_name: str) -> list[str]:
        """A python version of ed.

        Args:
            script (str): Ed commands to run.
            file_name (str): Script creates or edits this file.

        Returns:
            list[str]: The output of the script.
        """
        commands = script.split("\n")

        file_name = sanitize_path(file_name)

        file_path = self.root_folder + file_name
        if os.path.isfile(file_path):
            with open(file_path, encoding="utf-8") as f:
                self.buffer = Buffer(f.readlines())

        command_lines: list[tuple[Any, list[str]]] = []
        current_command = None
        current_list: list[str] = []

        for command, upcoming in zip(commands, commands[1:], strict=False):
            command = command.strip()
            if command.startswith("# "):
                # comments, because this is unreadable without them
                continue
            if not command:
                # blank commands are noise
                continue
            if command.startswith("e "):
                # can't really load right now
                continue
            if command == ".":
                if current_command is not None:
                    command_lines.append((current_command, current_list))

                self._run_commands(command_lines)
                current_command = None
                current_list = []
                command_lines = []
                continue

            if command == "q":
                # stop processing commands
                break
            if command == "w":
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(self.buffer.lines)
                continue

            if command.startswith("> "):
                # always a line
                current_list.append(f"{command[2:]}\n")
            else:
                if upcoming is None or not upcoming.startswith("> "):
                    current_command = command
                    command_lines.append((current_command, current_list))
                current_command = command
                current_list = []

            # always be running commands unless we're add/editing a line next.
            if upcoming is None:
                # last command, probably a q
                self._run_commands(command_lines)
            elif current_list or upcoming.startswith("> "):
                # waiting for . or expecting more lines
                pass
            else:
                self._run_commands(command_lines)

        return self.buffer.lines

    def _run_commands(self, command_lines: (list[tuple[Any, list[str]]])) -> None:
        """Run the commands.

        Args:
            command_lines (list[tuple[Any, list[str]]]): The commands to run.
        """
        for command_now, lines_now in command_lines:
            print(command_now, "\n".join(lines_now))
            self.buffer.run(command_now, lines_now)


if __name__ == "__main__":

    def run() -> None:
        """Example"""
        groceries = """
    a
    > milk
    a
    > eggs
    a
    > bread
    .
    w
    q
        """

        groceries = """a
    > Test Line 1
    .
    a
    > Test Line 2
    .
    w
    q"""
        groceries = """
    a
    > Line 1
    > Line 2
    .
    1d
    w
    q"""
        tool = EdTool(".", Config(".."))
        tool.ed(groceries, "groceries.txt")

    run()
