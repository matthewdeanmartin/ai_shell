"""
Directory listing tool, optimized for AI.
"""
import logging
import os
import time
from io import StringIO
from pathlib import Path
from typing import Optional, Union

from ai_shell.ai_logs.log_to_bash import log
from ai_shell.utils.config_manager import Config
from ai_shell.utils.cwd_utils import change_directory
from ai_shell.utils.read_fs import human_readable_size, is_file_in_root_folder, safe_glob, tree

logger = logging.getLogger(__name__)


class LsTool:
    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the FindTool class.

        Args:
            root_folder (str): The root folder path for file operations.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder
        self.config = config
        self.auto_cat = config.get_flag("auto_cat", True)

    @log()
    def ls_markdown(self, path: Optional[str] = ".", all_files: bool = False, long: bool = False) -> str:
        """List directory contents, with options to include all files and detailed view.

        Args:
            path (str, optional): The directory path to list. Defaults to the current directory '.'.
            all_files (bool): If True, include hidden files. Defaults to False.
            long (bool): If True, include details like permissions, owner, size, and modification date. Defaults to False.

        Returns:
            str: The markdown representation of the ls command output.
        """
        try:
            entries_info = self.ls(path, all_files, long)
        except (FileNotFoundError, NotADirectoryError):
            tree_text = tree(Path(os.getcwd()))
            markdown_content = f"# Bad `ls` command. Here are all the files you can see\n\n{tree_text}"
            return markdown_content

        output = StringIO()

        is_first = True
        for line in entries_info:
            if not is_first:
                output.write("\n")
            is_first = False
            output.write(line)

        output.seek(0)
        return output.read()

    @log()
    def ls(self, path: Optional[str] = None, all_files: bool = False, long: bool = False) -> Union[list[str], str]:
        """
        List directory contents, with options to include all files and detailed view.

        Args:
            path (str, optional): The directory path to list. Defaults to the current directory '.'.
            all_files (bool): If True, include hidden files. Defaults to False.
            long (bool): If True, include details like permissions, owner, size, and modification date. Defaults to False.

        Returns:
            List[str]: List of files and directories, optionally with details.
        """
        logger.info(f"ls --path {path} --all_files {all_files} --long  {long}")

        if path is None:
            path = ""

        if path is not None and ("?" in path or "*" in path or "[" in path or "]" in path):
            # Globs behave very different from non-globs. :(
            #  or "{" in path or "}"  <-- is this a glob pattern?
            entries = safe_glob(path, self.root_folder)
        else:
            try:
                # enumerate list to check if the path exists
                entries = list(
                    (_ for _ in os.listdir(path))
                    if all_files
                    else (entry for entry in os.listdir(path) if not entry.startswith("."))
                )
            except (FileNotFoundError, NotADirectoryError):
                # if not, just tell the bot everything.
                tree_text = tree(Path(os.getcwd()))
                markdown_content = f"# Bad `ls` command. Here are all the files you can see\n\n{tree_text}"
                return markdown_content
        entries_info = []

        for entry in entries:
            # is this None-safety here correct?
            full_path = entry if path is None else os.path.join(path, entry)
            if not is_file_in_root_folder(full_path, self.root_folder):
                continue
            if os.path.isdir(full_path) and entry.endswith("__pycache__"):
                continue
            if long:
                stats = os.stat(full_path)
                # Always human readable, too many tokens for byte count.
                size = human_readable_size(stats.st_size)
                mod_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(stats.st_mtime))
                entries_info.append(f"{size:} {mod_time} {entry}")
            else:
                entries_info.append(entry)
        if logger.level == logging.DEBUG:
            for line in entries_info:
                logger.debug(line)
        return entries_info


if __name__ == "__main__":

    def run() -> None:
        """Example"""
        with change_directory("src"):
            a = LsTool("src", config=Config(".."))
            results = a.ls(".")
            for row in results:
                print(row)
                if "__pycache__" in row:
                    raise TypeError(row)
            print(a.ls_markdown("."))

    run()
