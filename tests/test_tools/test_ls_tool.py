import pytest

from ai_shell.ls_tool import LsTool
from tests.util import config_for_tests


def create_test_files(directory, files):
    for file in files:
        (directory / file).touch()


@pytest.fixture
def test_directory(tmp_path):
    files = ["file1.txt", ".hidden1", "file2.txt", ".hidden2"]
    create_test_files(tmp_path, files)
    return tmp_path


def test_ls_basic(test_directory):
    lstool = LsTool(str(test_directory), config=config_for_tests())
    expected_files = ["file1.txt", "file2.txt"]
    assert sorted(lstool.ls(str(test_directory))) == sorted(expected_files)


def test_ls_basic_markdown(test_directory):
    lstool = LsTool(str(test_directory), config=config_for_tests())
    assert lstool.ls_markdown(str(test_directory)) == "file1.txt\nfile2.txt"


def test_ls_all(test_directory):
    lstool = LsTool(str(test_directory), config=config_for_tests())
    expected_files = ["file1.txt", ".hidden1", "file2.txt", ".hidden2"]
    assert sorted(lstool.ls(str(test_directory), all_files=True)) == sorted(expected_files)


def test_ls_long(test_directory):
    lstool = LsTool(str(test_directory), config=config_for_tests())
    result = lstool.ls(str(test_directory), long=True)
    assert len(result) == 2  # Two non-hidden files
    # More detailed checks can be added based on the format of the long listing


def test_ls_all_long(test_directory):
    lstool = LsTool(str(test_directory), config=config_for_tests())
    result = lstool.ls(str(test_directory), all_files=True, long=True)
    assert len(result) == 4  # Two files and two hidden files
    # More detailed checks can be added based on the format of the long listing


def test_ls_empty_directory(tmp_path):
    lstool = LsTool(str(tmp_path), config=config_for_tests())
    assert lstool.ls(str(tmp_path)) == []


def test_ls_invalid_directory():
    lstool = LsTool("/non/existent/directory", config=config_for_tests())
    # Was better to return textual info instead of error object.
    # with pytest.raises(OSError):
    result = lstool.ls("/non/existent/directory")
    assert result.startswith("# Bad")
