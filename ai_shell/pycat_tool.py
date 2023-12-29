"""
Cat, except optimized for python files.
"""
import logging
import os
from io import StringIO
from pathlib import Path

import python_minifier

from ai_shell.pyutils.validate import is_python_file
from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log
from ai_shell.utils.read_fs import is_file_in_root_folder, tree

logger = logging.getLogger(__name__)


class PyCatTool:
    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the PyCatTool with a root folder.

        Args:
            root_folder (str): The root folder path to start the file traversal from.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder
        self.config = config
        self.auto_cat = config.get_flag("auto_cat")

    @log()
    def format_code_as_markdown(
        self,
        base_path: str,
        header: str,
        no_docs: bool = False,
        no_comments: bool = False,
    ) -> str:
        """
        Combine all Python files in a directory into a single Markdown file.

        This method traverses the directory starting from base_path, and for each Python file found,
        its contents are formatted and appended to the Markdown file specified by output_file.

        Args:
            base_path (str): The base path of the directory to start traversing.
            header (str): A header string to be included at the beginning of the Markdown file.
            no_docs (bool): Whether to exclude docstrings from the output. Defaults to False.
            no_comments (bool): Whether to exclude comments from the output. Defaults to False.

        Returns:
            str: The Markdown file contents.
        """
        output_file = StringIO()
        if header == "tree":
            tree_text = tree(Path(base_path))
            markdown_content = f"# Source Code Filesystem Tree\n\n{tree_text}"
            output_file.write(markdown_content)

        markdown_content = f"# {header} Source Code\n\n"

        for root, _dirs, files in os.walk(base_path):
            for file in files:
                if not is_file_in_root_folder(file, self.root_folder):
                    continue
                if is_python_file(file):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, base_path)
                    markdown_content += format_path_as_header(relative_path)
                    markdown_content += "```python\n"
                    markdown_content += read_file_contents(full_path)
                    markdown_content += "\n```\n\n"
        output_file.write(markdown_content)
        return output_file.getvalue()


def format_path_as_header(path: str) -> str:
    """
    Format a file path as a Markdown header.

    Args:
        path (str): The file path to format.

    Returns:
        str: The formatted path as a Markdown header.
    """
    return f"## {path}\n\n"


def read_file_contents(file_path: str) -> str:
    """
    Read the contents of a file and return as a string.

    Args:
        file_path (str): The path of the file to read.

    Returns:
        str: The contents of the file.
    """
    with open(file_path, encoding="utf-8") as file:
        return file.read()


def strip_docstrings(source_code: str) -> str:
    """
    Strip docstrings from a given Python source code.

    Args:
        source_code (str): The Python source code as a string.

    Returns:
        str: The Python source code with docstrings removed.
    """
    return python_minifier.minify(
        source_code,
        remove_annotations=True,
        remove_literal_statements=True,
        rename_locals=False,
        rename_globals=False,
        hoist_literals=False,
    )


if __name__ == "__main__":

    def run() -> None:
        with open(__file__, encoding="utf-8") as file:
            source_code = file.read()

        stripped_code = strip_docstrings(source_code)
        print(stripped_code)

    run()
