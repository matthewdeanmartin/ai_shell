# Example usage
from ai_shell.utils.read_fs import sanitize_path


def test_sanitize_path():
    # some_folder/some_file.txt
    # another_folder\another_file.txt
    # file.txt
    assert sanitize_path("../some_folder/some_file.txt") == "some_folder/some_file.txt"
    assert sanitize_path("..\\..\\another_folder\\another_file.txt") == "another_folder\\another_file.txt"
    assert sanitize_path("./file.txt") == "file.txt"
