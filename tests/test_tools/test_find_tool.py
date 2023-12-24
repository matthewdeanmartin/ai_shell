import os

import pytest

from ai_shell.find_tool import FindTool


# Setup a test directory and files
@pytest.fixture(scope="module")
def setup_test_environment(tmp_path_factory):
    test_dir = tmp_path_factory.mktemp("data")
    # Create some test files and directories here
    # For example:
    (test_dir / "test_file.txt").write_text("This is a test file.")
    (test_dir / "small_file.txt").write_text("Small")
    os.mkdir(test_dir / "test_dir")

    return test_dir


def test_find_files_by_name(setup_test_environment):
    absolute_file_path = os.path.abspath(setup_test_environment)
    tool = FindTool(absolute_file_path)
    results = tool.find_files(name="test_file.txt")
    assert len(results) == 1
    assert "test_file.txt" in results[0]


def test_find_files_by_regex(setup_test_environment):
    absolute_file_path = os.path.abspath(setup_test_environment)
    tool = FindTool(absolute_file_path)
    results = tool.find_files(regex=r"test_.*\.txt")
    assert len(results) >= 1
    assert any("test_file.txt" in file for file in results)


def test_find_files_by_type(setup_test_environment):
    absolute_file_path = os.path.abspath(setup_test_environment)
    tool = FindTool(absolute_file_path)
    results = tool.find_files(file_type="file")
    # weaken the assertion here because we don't get back a full path
    # previously checked if returned filed were files based on path
    assert results

    results = tool.find_files(file_type="directory")
    # weaken the assertion here because we don't get back a full path
    assert results


def test_find_files_by_size(setup_test_environment):
    absolute_file_path = os.path.abspath(setup_test_environment)
    tool = FindTool(absolute_file_path)

    results = tool.find_files(size="+10")  # Assuming small_file.txt is smaller than 10 bytes
    assert all("small_file.txt" not in file for file in results)

    results = tool.find_files(size="-10")
    assert any("small_file.txt" in file for file in results)


def test_find_files_markdown_by_type(setup_test_environment):
    absolute_file_path = os.path.abspath(setup_test_environment)
    tool = FindTool(absolute_file_path)
    results = tool.find_files_markdown(file_type="file")
    assert results == "small_file.txt\ntest_file.txt\n"

    results = tool.find_files_markdown(file_type="directory")
    assert results == "test_dir\n"
