"""
This module contains functions related to file system operations.
"""
import os
import shutil


def empty_folder(folder_path: str) -> None:
    """
    Empty the folder at the given path

    Args:
        folder_path (str): Path to the folder to be emptied
    """
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        os.makedirs(folder_path, exist_ok=True)


def clear_data(log_folder: str, db_path: str) -> None:
    """
    Clear the database and log files
    """
    # Code to clear the database and log files
    empty_folder(log_folder)
    os.remove(db_path)


def get_containing_folder_path(file_path: str) -> str:
    """
    Get the absolute path of the folder containing the given file.

    Args:
        file_path (str): Path to the file (__file__)

    Returns:
        str: Absolute path of the containing folder
    """
    return os.path.abspath(os.path.dirname(file_path))


def is_git_repo(path: str) -> bool:
    """
    Check if the path is inside a git repository by looking for a .git directory.

    Args:
        path (str): The directory path to check.

    Returns:
        bool: True if inside a git repo, False otherwise.
    """
    current_path = path
    while current_path != os.path.dirname(current_path):
        if os.path.isdir(os.path.join(current_path, ".git")):
            return True
        current_path = os.path.dirname(current_path)
    return False


def prompt_and_update_gitignore(repo_path: str) -> None:
    """Prompt the user to ignore logs and update .gitignore accordingly."""
    if not is_git_repo(repo_path):
        return

    gitignore_path = os.path.join(repo_path, ".gitignore")

    # Check if .gitignore exists and 'logs' is already listed
    if os.path.exists(gitignore_path):
        with open(gitignore_path, encoding="utf-8") as file:
            if "logs" in file.read():
                print("'logs' directory is already ignored in .gitignore.")
                return

    # Prompt user for action
    response = (
        input("This directory is a Git repository. Do you want to ignore 'logs' directory? (y/n): ").strip().lower()
    )
    if (response.lower() + "xxx")[0] == "y":
        with open(gitignore_path, "a", encoding="utf-8") as file:
            file.write("\nlogs/")
        print("'logs' directory is now ignored in .gitignore.")
    else:
        print("No changes made to .gitignore.")
