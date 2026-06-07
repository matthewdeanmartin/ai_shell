import os
import subprocess
import tempfile

import pytest

from ai_shell.git_tool import GitTool
from tests.util import config_for_tests


def _git(repo_dir, *args):
    """Run a git command in repo_dir for test setup."""
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    return subprocess.run(
        ["git", "-C", repo_dir, *args], capture_output=True, text=True, check=True, env=env
    ).stdout.strip()


@pytest.fixture(scope="module")
def test_repo():
    repo_dir = tempfile.mkdtemp()
    _git(repo_dir, "init")
    _git(repo_dir, "checkout", "-b", "main")

    gitignore_path = os.path.join(repo_dir, ".gitignore")
    with open(gitignore_path, "w") as f:
        f.write("*.log\n*.tmp\n")

    for filename in ["test.txt", "ignored.log", "another.tmp"]:
        open(os.path.join(repo_dir, filename), "w").close()

    # ignored.log / another.tmp match .gitignore, so git won't add them — that's fine.
    _git(repo_dir, "add", "test.txt", ".gitignore")
    _git(repo_dir, "commit", "-m", "Initial commit")
    return repo_dir


def test_init(test_repo):
    tool = GitTool(test_repo, config=config_for_tests())
    assert tool.repo_path == test_repo


def test_is_ignored_by_gitignore(test_repo):
    tool = GitTool(test_repo, config=config_for_tests())
    assert tool.is_ignored_by_gitignore(os.path.join(test_repo, "ignored.log")) is True
    assert tool.is_ignored_by_gitignore(os.path.join(test_repo, "test.txt")) is False


def test_git_status(test_repo):
    tool = GitTool(test_repo, config=config_for_tests())

    untracked_file = os.path.join(test_repo, "untracked.txt")
    with open(untracked_file, "w") as f:
        f.write("untracked content")

    status = tool.git_status()
    assert "untracked.txt" in status["untracked_files"]


def test_git_diff(test_repo):
    tool = GitTool(test_repo, config=config_for_tests())
    assert tool.git_diff() is not None


def test_git_log_file(test_repo):
    tool = GitTool(test_repo, config=config_for_tests())
    file_path = os.path.join(test_repo, "log.txt")
    with open(file_path, "w") as f:
        f.write("initial content")
    _git(test_repo, "add", "log.txt")
    _git(test_repo, "commit", "-m", "Initial commit for log")
    assert tool.git_log_file("log.txt") is not None


def test_git_log_search(test_repo):
    tool = GitTool(test_repo, config=config_for_tests())
    unique_message = "Unique commit message for search"
    file_path = os.path.join(test_repo, "search.txt")
    with open(file_path, "w") as f:
        f.write("content")
    _git(test_repo, "add", "search.txt")
    _git(test_repo, "commit", "-m", unique_message)
    assert tool.git_log_search("content") is not None


def test_git_show(test_repo):
    tool = GitTool(test_repo, config=config_for_tests())
    assert tool.git_show() is not None


def test_get_current_branch(test_repo):
    tool = GitTool(test_repo, config=config_for_tests())
    _git(test_repo, "checkout", "-B", "test-branch")
    assert tool.get_current_branch() == "test-branch"
    _git(test_repo, "checkout", "main")


def test_get_recent_commits(test_repo):
    tool = GitTool(test_repo, config=config_for_tests())
    _git(test_repo, "checkout", "main")
    for i in range(5):
        file_path = os.path.join(test_repo, f"file{i}.txt")
        with open(file_path, "w") as f:
            f.write(f"content {i}")
        _git(test_repo, "add", f"file{i}.txt")
        _git(test_repo, "commit", "-m", f"Commit {i}")

    recent_commits = tool.get_recent_commits(3)
    assert len(recent_commits) == 3


def test_git_diff_commit(test_repo):
    tool = GitTool(test_repo, config=config_for_tests())
    _git(test_repo, "checkout", "main")
    commit1 = _git(test_repo, "rev-parse", "HEAD")
    file_path2 = os.path.join(test_repo, "diffcommit.txt")
    with open(file_path2, "w") as f:
        f.write("more content")
    _git(test_repo, "add", "diffcommit.txt")
    _git(test_repo, "commit", "-m", "Second commit")
    commit2 = _git(test_repo, "rev-parse", "HEAD")
    assert tool.git_diff_commit(commit1, commit2) is not None
