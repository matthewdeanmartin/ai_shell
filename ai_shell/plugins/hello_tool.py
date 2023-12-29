"""
Plugin Example
"""

from ai_shell.utils.logging_utils import log


class HelloTool:
    """A python version of ed."""

    def __init__(self, root_folder: str, config: dict[str, str]) -> None:
        """
        Initialize the HelloTool class.

        Args:
            root_folder (str): The root folder path for file operations.
            config (dict[str,str]): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder if root_folder.endswith("/") else root_folder + "/"
        self.config = config

    @log()
    def hello(self) -> str:
        """Says hello.

        Returns:
            str: The output of the script.
        """
        return "Hello, world!"

    @log()
    def goodbye(self) -> str:
        """Says goodbye.

        Returns:
            str: The output of the script.
        """
        return "Bye, world!"

    @log()
    def with_args(self, an_int: int, a_float: float, a_str: str) -> str:
        """Says goodbye.

        Args:
            an_int (int): An integer.
            a_float (float): A float.
            a_str (str): A string.

        Returns:
            str: The output of the script.
        """
        return f"an_int={an_int}, a_float={a_float}, a_str={a_str}"
