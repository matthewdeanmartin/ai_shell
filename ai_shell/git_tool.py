"""
Read-only git queries by shelling out to the git CLI.

These are intentionally read-only (status/diff/log/show/branch). We shell out via
``safe_subprocess`` (``shell=False``) rather than depend on GitPython, which is
just sugar over the same commands.
"""

import fnmatch
import logging
import os
import shlex
from typing import Any

from ai_shell.ai_logs.log_to_bash import log
from ai_shell.externals.subprocess_utils import CommandResult, safe_subprocess
from ai_shell.utils.config_manager import Config

logger = logging.getLogger(__name__)


class GitTool:
    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the GitTool class.

        Args:
            root_folder (str): The root folder path for repo operations.
            config (Config): The developer input that bot shouldn't set.
        """
        self.repo_path = root_folder
        self.config = config
        self.auto_cat = config.get_flag("auto_cat", True)
        self.utf8_errors = config.get_value("utf8_errors", "surrogateescape")

    def _git(self, args: str) -> CommandResult:
        """Run a git command against the repo and return its result.

        Args:
            args (str): The git subcommand and arguments (already shell-safe).

        Returns:
            CommandResult: stdout/stderr/return_code of the command.
        """
        repo = shlex.quote(os.path.abspath(self.repo_path))
        result = safe_subprocess("git", f"-C {repo} {args}")
        if result.return_code != 0:
            logger.warning("git %s failed: %s", args, result.stderr)
        return result

    def is_ignored_by_gitignore(self, file_path: str, gitignore_path: str = ".gitignore") -> bool:
        """
        Check if a file is ignored by .gitignore.

        Args:
            file_path (str): The path of the file to check.
            gitignore_path (str): The path to the .gitignore file. Defaults to '.gitignore' in the current directory.

        Returns:
            bool: True if the file is ignored, False otherwise.

        Raises:
            FileNotFoundError: If the .gitignore file is not found.
        """
        full_gitignore_path = os.path.join(self.repo_path, gitignore_path)

        if not os.path.isfile(full_gitignore_path):
            raise FileNotFoundError(f"No .gitignore file found at {full_gitignore_path}")

        file_path = os.path.abspath(file_path)

        with open(full_gitignore_path, encoding="utf-8", errors=self.utf8_errors) as gitignore:
            for line in gitignore:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                gitignore_pattern = os.path.join(os.path.dirname(gitignore_path), line)
                if fnmatch.fnmatch(file_path, gitignore_pattern):
                    return True
        return False

    @log()
    def git_status(self) -> dict[str, Any]:
        """Returns the status of the repository.

        Returns:
            dict[str, Any]: Structured `git status` response
        """
        result = self._git("status --porcelain")
        changed_files: list[str] = []
        untracked_files: list[str] = []
        for line in result.stdout.splitlines():
            if not line:
                continue
            # porcelain format: 2-char status code, a space, then the path
            path = line[3:].strip()
            if line.startswith("??"):
                untracked_files.append(path)
            else:
                changed_files.append(path)
        return {"changed_files": changed_files, "untracked_files": untracked_files}

    @log()
    def get_current_branch(self) -> str:
        """
        Retrieves the current branch name of the repository.

        Returns:
            str: The current branch name.
        """
        return self._git("branch --show-current").stdout.strip()

    @log()
    def get_recent_commits(self, n: int = 10, short_hash: bool = False) -> list[dict[str, Any]]:
        """
        Retrieves the most recent commit hashes from the current branch.

        Args:
            n (int, optional): The number of recent commits to retrieve. Defaults to 10.
            short_hash (bool, optional): If True, also return short hashes. Defaults to False.

        Returns:
            list[dict[str, Any]]: One dict per commit with a 'full_hash' (and
                                  'short_hash' when requested).
        """
        result = self._git(f"log --pretty=format:%H -n {int(n)}")
        hashes = [h for h in result.stdout.splitlines() if h]
        if short_hash:
            return [{"short_hash": h[:7], "full_hash": h} for h in hashes]
        return [{"full_hash": h} for h in hashes]

    @log()
    def git_diff(self) -> list[dict[str, Any]]:
        """Returns the differences in the working directory.

        Returns:
            list[dict[str, Any]]: Structured `git diff` response
        """
        diffs = self._git("diff HEAD --name-only").stdout.splitlines()
        return [{"file": diff} for diff in diffs if diff]

    @log()
    def git_log_file(self, filename: str) -> list[dict[str, Any]]:
        """Returns the commit history for a specific file.

        Args:
            filename (str): The path to the file.

        Returns:
            list[dict[str, Any]]: Structured `git log` response
        """
        result = self._git(f"log --pretty=format:%H - %an, %ar : %s -- {shlex.quote(filename)}")
        commits = [c for c in result.stdout.splitlines() if c]
        return [{"commit": commit} for commit in commits]

    @log()
    def git_log_search(self, search_string: str) -> list[dict[str, Any]]:
        """Returns the commit history that matches the search string.

        Args:
            search_string (str): The search string.

        Returns:
            list of dict: Structured `git log` response
        """
        result = self._git(f"log -S {shlex.quote(search_string)} --pretty=format:%H - %an, %ar : %s")
        commits = [c for c in result.stdout.splitlines() if c]
        return [{"commit": commit} for commit in commits]

    @log()
    def git_show(self) -> list[dict[str, Any]]:
        """Shows various types of objects (commits, tags, etc.).

        Returns:
            list[dict[str, Any]]: Structured `git show` response
        """
        result = self._git("show --no-patch --pretty=format:%H - %an, %ar : %s")
        show_data = [d for d in result.stdout.splitlines() if d]
        return [{"data": data} for data in show_data]

    @log()
    def git_diff_commit(self, commit1: str, commit2: str) -> list[dict[str, Any]]:
        """Shows changes between two commits.

        Args:
            commit1 (str): First commit
            commit2 (str): Second commit

        Returns:
            list[dict[str, Any]]: Structured `git diff` response
        """
        result = self._git(f"diff {shlex.quote(commit1)} {shlex.quote(commit2)} --name-only")
        diffs = [d for d in result.stdout.splitlines() if d]
        return [{"file": diff} for diff in diffs]
