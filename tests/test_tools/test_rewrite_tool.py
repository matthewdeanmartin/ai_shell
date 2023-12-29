import pytest

from ai_shell.rewrite_tool import RewriteTool
from tests.util import config_for_tests
import ai_shell


def test_write_new_file_success(tmp_path):
    with ai_shell.change_directory(str(tmp_path)):
        tool = RewriteTool(str(tmp_path), config=config_for_tests())
        tool.auto_cat = False
        file_path = "test_file.txt"
        content = "Hello, world!"
        message = tool.write_new_file(file_path, content)

        assert "File written to" in message
        assert file_path in message
        with open(tmp_path / file_path) as file:
            assert file.read() == content


def test_write_new_file_failure_file_exists(tmp_path):
    with ai_shell.change_directory(str(tmp_path)):
        tool = RewriteTool(str(tmp_path), config=config_for_tests())
        file_path = "test_file.txt"
        content = "Hello, world!"
        (tmp_path / file_path).write_text(content)

        with pytest.raises(ValueError) as excinfo:
            tool.write_new_file(file_path, "New content")

        assert "File already exists" in str(excinfo.value)


def test_write_new_file_failure_outside_root(tmp_path):
    with ai_shell.change_directory(str(tmp_path)):
        tool = RewriteTool(str(tmp_path), config=config_for_tests())
        file_path = "/outside_test_file.txt"

        with pytest.raises(ValueError) as excinfo:
            tool.write_new_file(file_path, "Some content")

        assert "File path must be within the root folder" in str(excinfo.value)


def test_rewrite_file_success(tmp_path):
    with ai_shell.change_directory(str(tmp_path)):
        tool = RewriteTool(str(tmp_path), config=config_for_tests())
        tool.auto_cat = False
        file_path = "test_file.txt"
        original_content = "Original content"
        (tmp_path / file_path).write_text(original_content)

        new_content = "Updated content"
        message = tool.rewrite_file(file_path, new_content)

        assert message == f"File rewritten to {file_path}, please view to verify contents."
        with open(tmp_path / file_path) as file:
            assert file.read() == new_content


def test_rewrite_file_failure_file_not_exists(tmp_path):
    with ai_shell.change_directory(str(tmp_path)):
        tool = RewriteTool(str(tmp_path), config=config_for_tests())
        file_path = "nonexistent_file.txt"

        with pytest.raises(FileNotFoundError) as excinfo:
            tool.rewrite_file(file_path, "Some content")
        # File does not exist, use ls tool to see what files there are.
        assert "File does not exist" in str(excinfo.value)


def test_rewrite_file_failure_outside_root(tmp_path):
    with ai_shell.change_directory(str(tmp_path)):
        tool = RewriteTool(str(tmp_path), config=config_for_tests())
        file_path = "/outside_test_file.txt"

        with pytest.raises(ValueError) as excinfo:
            tool.rewrite_file(file_path, "Some content")

        assert "File path must be within the root folder" in str(excinfo.value)
