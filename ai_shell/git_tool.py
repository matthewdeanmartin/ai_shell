"""
Wrapper around GitPython and shell commands to git.
"""
import fnmatch
import logging
import os
from typing import Any

from git import Repo

from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log

logger = logging.getLogger(__name__)


# TODO: Support automatically adding a branch on start of session.
class GitTool:
    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the GitTool class.

        Args:
            root_folder (str): The root folder path for repo operations.
            config (Config): The developer input that bot shouldn't set.
        """
        # Initialize the repository
        self.repo_path = root_folder
        self.repo = Repo(root_folder)
        self.config = config
        self.auto_cat = config.get_flag("auto_cat")

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
        # Resolve the full path to the .gitignore file
        full_gitignore_path = os.path.join(self.repo_path, gitignore_path)

        if not os.path.isfile(full_gitignore_path):
            raise FileNotFoundError(f"No .gitignore file found at {full_gitignore_path}")

        # Normalize file path
        file_path = os.path.abspath(file_path)

        with open(full_gitignore_path, encoding="utf-8") as gitignore:
            for line in gitignore:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Convert the .gitignore pattern to a glob pattern
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
        logger.info("git status")
        changed_files = [item.a_path for item in self.repo.index.diff(None)]
        untracked_files = self.repo.untracked_files
        return {"changed_files": changed_files, "untracked_files": untracked_files}

    @log()
    def get_current_branch(
        self,
    ) -> str:
        """
        Retrieves the current branch name of the repository.

        Returns:
            str: The current branch name.
        """
        logger.info("git branch --show-current")
        return self.repo.active_branch.name

    @log()
    def get_recent_commits(self, n: int = 10, short_hash: bool = False) -> list[dict[str, Any]]:
        """
        Retrieves the most recent commit hashes from the current branch.

        Args:
            n (int, optional): The number of recent commits to retrieve. Defaults to 10.
            short_hash (bool, optional): If True, return short hashes; otherwise, return full hashes. Defaults to False.

        Returns:
            list[dict[str, Any]]: A list of dictionaries, each containing 'short_hash' and 'full_hash' keys (if short_hash is True),
                          or only 'full_hash' (if short_hash is False), representing the commit hashes.
        """
        logger.info(f"git log --pretty=format:%H -n {n}")
        current_branch = self.get_current_branch()
        commits = list(self.repo.iter_commits(current_branch, max_count=n))
        if short_hash:
            return [{"short_hash": commit.hexsha[:7], "full_hash": commit.hexsha} for commit in commits]
        return [{"full_hash": commit.hexsha} for commit in commits]

    @log()
    def git_diff(self) -> list[dict[str, Any]]:
        """Returns the differences in the working directory.

        Returns:
            list[dict[str, Any]]: Structured `git diff` response
        """
        logger.info("git diff --name-only")
        diffs = self.repo.git.diff("HEAD", name_only=True).splitlines()
        return [{"file": diff} for diff in diffs]

    @log()
    def git_log_file(self, filename: str) -> list[dict[str, Any]]:
        """Returns the commit history for a specific file.

        Args:
            filename (str): The path to the file.

        Returns:
            list[dict[str, Any]]: Structured `git log` response
        """
        logger.info(f"git log --pretty=format:%H -n 1 {filename}")
        commits = self.repo.git.log("--pretty=format:%H - %an, %ar : %s", filename).splitlines()
        return [{"commit": commit} for commit in commits]

    @log()
    def git_log_search(self, search_string: str) -> list[dict[str, Any]]:
        """Returns the commit history that matches the search string.

        Args:
            search_string (str): The search string.

        Returns:
            list of dict: Structured `git log` response
        """
        logger.info(f"git log --pretty=format:%H -S {search_string}")
        commits = self.repo.git.log("-S", search_string, "--pretty=format:%H - %an, %ar : %s").splitlines()
        return [{"commit": commit} for commit in commits]

    @log()
    def git_show(self) -> list[dict[str, Any]]:
        """Shows various types of objects (commits, tags, etc.).

        Returns:
            list[dict[str, Any]]: Structured `git show` response
        """
        logger.info("git show --pretty=format:%H -n 1")
        show_data = self.repo.git.show("--pretty=format:%H - %an, %ar : %s", n=1).splitlines()
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
        logger.info(f"git diff --name-only {commit1} {commit2}")
        diffs = self.repo.git.diff(commit1, commit2, name_only=True).splitlines()
        return [{"file": diff} for diff in diffs]


if __name__ == "__main__":

    def run() -> None:
        """Test run"""
        tool = GitTool("..", config=Config(".."))
        current_branch = tool.get_current_branch()
        print(f"Current branch: {current_branch}")
        recent = tool.get_recent_commits(5, short_hash=True)
        print(recent)
        print(tool.git_status())
        print(tool.git_diff())
        print(tool.git_log_file(__file__))
        print(tool.git_log_search("README"))
        print(tool.git_show())
        print(tool.git_diff_commit(recent[0]["short_hash"], recent[1]["short_hash"]))

    run()
