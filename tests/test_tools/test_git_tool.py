import os
import tempfile

import pytest
from git import Repo

from ai_shell.git_tool import GitTool


@pytest.fixture(scope="module")
def test_repo():
    # Setup a temporary directory as a git repository
    repo_dir = tempfile.mkdtemp()
    repo = Repo.init(repo_dir)

    # Create a .gitignore file in the repository
    gitignore_path = os.path.join(repo_dir, ".gitignore")
    with open(gitignore_path, "w") as f:
        f.write("*.log\n*.tmp\n")

    # Add some files
    filenames = ["test.txt", "ignored.log", "another.tmp"]
    for filename in filenames:
        open(os.path.join(repo_dir, filename), "w").close()

    repo.index.add(filenames)
    repo.index.commit("Initial commit")

    return repo_dir


def test_init(test_repo):
    tool = GitTool(test_repo)
    assert tool.repo_path == test_repo
    assert tool.repo is not None


def test_is_ignored_by_gitignore(test_repo):
    tool = GitTool(test_repo)
    assert tool.is_ignored_by_gitignore(os.path.join(test_repo, "ignored.log")) is True
    assert tool.is_ignored_by_gitignore(os.path.join(test_repo, "test.txt")) is False


def test_git_status(test_repo):
    tool = GitTool(test_repo)

    # Create a changed file and add it to the staging area
    changed_file = os.path.join(test_repo, "changed.txt")
    with open(changed_file, "w") as f:
        f.write("changed content")
    tool.repo.index.add([changed_file])

    # Create an untracked file without adding it to the staging area
    untracked_file = os.path.join(test_repo, "untracked.txt")
    with open(untracked_file, "w") as f:
        f.write("untracked content")

    status = tool.git_status()

    # Assuming changed_files refers to unstaged changes
    tool.repo.index.commit("Test commit")
    tool.git_status()

    # Convert the absolute paths to relative paths
    relative_untracked_file = os.path.relpath(untracked_file, test_repo)
    relative_changed_file = os.path.relpath(changed_file, test_repo)

    assert relative_untracked_file in status["untracked_files"]
    assert relative_changed_file not in status["changed_files"]


def test_git_diff(test_repo):
    tool = GitTool(test_repo)

    # Modify a file
    modified_file = os.path.join(test_repo, "modified.txt")
    with open(modified_file, "w") as f:
        f.write("new content")

    # Call git_diff and check for no errors
    assert tool.git_diff() is not None


def test_git_log_file(test_repo):
    tool = GitTool(test_repo)
    file_path = os.path.join(test_repo, "log.txt")
    with open(file_path, "w") as f:
        f.write("initial content")
    tool.repo.index.add([file_path])
    tool.repo.index.commit("Initial commit for log")

    # Call git_log_file and check for no errors
    assert tool.git_log_file(file_path) is not None


def test_git_log_search(test_repo):
    tool = GitTool(test_repo)
    unique_message = "Unique commit message for search"
    file_path = os.path.join(test_repo, "search.txt")
    with open(file_path, "w") as f:
        f.write("content")
    tool.repo.index.add([file_path])
    tool.repo.index.commit(unique_message)

    # Call git_log_search and check for no errors
    assert tool.git_log_search(unique_message) is not None


def test_git_show(test_repo):
    tool = GitTool(test_repo)

    # Call git_show and check for no errors
    assert tool.git_show() is not None


def test_get_current_branch(test_repo):
    tool = GitTool(test_repo)
    branch_name = "test-branch"
    tool.repo.git.checkout("-b", branch_name)

    current_branch = tool.get_current_branch()
    assert current_branch == branch_name


def test_get_recent_commits(test_repo):
    tool = GitTool(test_repo)
    # Create some commits
    for i in range(5):
        file_path = os.path.join(test_repo, f"file{i}.txt")
        with open(file_path, "w") as f:
            f.write(f"content {i}")
        tool.repo.index.add([file_path])
        tool.repo.index.commit(f"Commit {i}")

    recent_commits = tool.get_recent_commits(3)
    assert len(recent_commits) == 3
    # Optionally, check the content of the commits


def test_git_diff_commit(test_repo):
    tool = GitTool(test_repo)

    # First commit
    file_path1 = os.path.join(test_repo, "file1.txt")
    with open(file_path1, "w") as f:
        f.write("initial content")
    tool.repo.index.add([file_path1])
    commit1 = tool.repo.index.commit("First commit")

    # Second commit
    file_path2 = os.path.join(test_repo, "file2.txt")
    with open(file_path2, "w") as f:
        f.write("more content")
    tool.repo.index.add([file_path2])
    commit2 = tool.repo.index.commit("Second commit")

    # Call git_diff_commit and check for no errors
    assert tool.git_diff_commit(commit1.hexsha, commit2.hexsha) is not None
