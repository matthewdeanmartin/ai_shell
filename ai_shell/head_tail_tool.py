"""
AI optimized head/tail tool
"""
import logging
from typing import Optional

from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log
from ai_shell.utils.read_fs import is_file_in_root_folder

logger = logging.getLogger(__name__)


class HeadTailTool:
    def __init__(self, root_folder: str, config: Config) -> None:
        """Initialize the HeadTailTool with a root folder.

        Args:
            root_folder (str): The root folder where files will be checked.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder
        self.config = config
        self.auto_cat = config.get_flag("auto_cat")

    @log()
    def head_markdown(self, file_path: str, lines: int = 10) -> str:
        """Return the first 'lines' lines of a file formatted as markdown.

        Args:
            file_path (str): Path to the file.
            lines (int): Number of lines to return. Defaults to 10.

        Returns:
            str: String containing the first 'lines' lines of the file.
        """
        return "\n".join(self.head(file_path, lines))

    @log()
    def head(self, file_path: str, lines: int = 10, byte_count: Optional[int] = None) -> list[str]:
        """Return the first 'lines' or 'byte_count' from a file.

        Args:
            file_path (str): Path to the file.
            lines (int): Number of lines to return. Ignored if byte_count is specified. Defaults to 10.
            byte_count (Optional[int]): Number of bytes to return. If specified, overrides lines.

        Returns:
            list[str]: Lines or byte_count of bytes from the start of the file.
        """
        return self.head_tail(file_path, lines, "head", byte_count)

    @log()
    def tail_markdown(self, file_path: str, lines: int = 10) -> str:
        """Return the last 'lines' lines of a file formatted as markdown.

        Args:
            file_path (str): Path to the file.
            lines (int): Number of lines to return. Defaults to 10.

        Returns:
            str: String containing the last 'lines' lines of the file.
        """
        return "\n".join(self.tail(file_path, lines))

    @log()
    def tail(self, file_path: str, lines: int = 10, byte_count: Optional[int] = None) -> list[str]:
        """Return the last 'lines' or 'bytes' from a file.

        Args:
            file_path (str): Path to the file.
            lines (int): Number of lines to return. Ignored if byte_count is specified. Defaults to 10.
            byte_count (Optional[int]): Number of bytes to return. If specified, overrides lines.

        Returns:
            list[str]: Lines or bytes from the end of the file.
        """
        return self.head_tail(file_path, lines, "tail", byte_count)

    def head_tail(
        self, file_path: str, lines: int = 10, mode: str = "head", byte_count: Optional[int] = None
    ) -> list[str]:
        """Read lines or bytes from the start ('head') or end ('tail') of a file.

        Args:
            file_path (str): Path to the file.
            lines (int): Number of lines to read. Ignored if byte_count is specified. Defaults to 10.
            mode (str): Operation mode, either 'head' or 'tail'. Defaults to 'head'.
            byte_count (Optional[int]): Number of bytes to read. If specified, overrides lines.

        Returns:
            list[str]: Requested lines or bytes from the file.

        Raises:
            ValueError: If mode is not 'head' or 'tail'.
            FileNotFoundError: If the file is not found in the root folder.
        """
        if mode == "head":
            logger.info(f"head --file_path {file_path} --lines {lines}")
        else:
            logger.info(f"tail --file_path {file_path} --lines {lines}")
        if mode not in ["head", "tail"]:
            raise ValueError("Mode must be 'head' or 'tail'")

        if not is_file_in_root_folder(file_path, self.root_folder):
            raise FileNotFoundError(f"File {file_path} not found in root folder {self.root_folder}")

        with open(file_path, "rb") as file:
            if byte_count is not None:
                if mode == "head":
                    return [file.read(byte_count).decode()]
                # mode == 'tail'
                file.seek(-byte_count, 2)  # Seek from end of file
                return [file.read(byte_count).decode()]

            # Read by lines if byte_count is not specified
            if mode == "head":
                return [next(file).decode("utf-8").rstrip("\r\n") for _ in range(lines)]
            # mode == 'tail'
            return [line.decode("utf-8").rstrip("\r\n") for line in list(file)[-lines:]]
