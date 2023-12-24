import pytest

from ai_shell.utils.read_fs import remove_root_folder


def test_remove_root_folder_with_absolute_paths(tmp_path):
    # Creating a temporary directory structure
    root_folder = tmp_path / "root"
    root_folder.mkdir()
    sub_folder = root_folder / "subfolder"
    sub_folder.mkdir()
    file_path = sub_folder / "test_file.txt"
    file_path.touch()

    # Running the test
    assert remove_root_folder(str(file_path), str(root_folder)) == "subfolder/test_file.txt"


def test_remove_root_folder_with_relative_paths(tmp_path):
    # Creating a temporary directory structure
    root_folder = tmp_path / "root"
    root_folder.mkdir()
    sub_folder = root_folder / "subfolder"
    sub_folder.mkdir()
    file_path = sub_folder / "test_file.txt"
    file_path.touch()

    # Running the test
    assert remove_root_folder("subfolder/test_file.txt", str(root_folder)) == "subfolder/test_file.txt"


def test_remove_root_folder_with_same_paths(tmp_path):
    # Creating a temporary directory
    root_folder = tmp_path / "root"
    root_folder.mkdir()

    # Running the test
    assert remove_root_folder(str(root_folder), str(root_folder)) == "."


def test_remove_root_folder_path_not_under_root(tmp_path):
    # Creating a temporary directory structure
    root_folder = tmp_path / "root"
    root_folder.mkdir()
    other_folder = tmp_path / "other"
    other_folder.mkdir()
    file_path = other_folder / "test_file.txt"
    file_path.touch()

    # Running the test
    with pytest.raises(ValueError):
        remove_root_folder(str(file_path), str(root_folder))
