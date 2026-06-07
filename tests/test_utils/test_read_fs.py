# Example usage
from ai_shell.utils.read_fs import is_file_in_root_folder, sanitize_path


def test_sanitize_path():
    # some_folder/some_file.txt
    # another_folder\another_file.txt
    # file.txt
    assert sanitize_path("../some_folder/some_file.txt") == "some_folder/some_file.txt"
    assert sanitize_path("..\\..\\another_folder\\another_file.txt") == "another_folder\\another_file.txt"
    assert sanitize_path("./file.txt") == "file.txt"


def test_is_file_in_root_folder_rejects_rooted_path_without_drive(tmp_path):
    assert is_file_in_root_folder("/outside_test_file.txt", str(tmp_path)) is False
