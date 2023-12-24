import pytest

from ai_shell.rewrite_tool import RewriteTool


def test_write_new_file_success(tmp_path):
    tool = RewriteTool(str(tmp_path))
    tool.auto_cat = False
    file_path = "test_file.txt"
    content = "Hello, world!"
    message = tool.write_new_file(file_path, content)

    assert message == f"File written to {tmp_path / file_path}"
    with open(tmp_path / file_path) as file:
        assert file.read() == content


def test_write_new_file_failure_file_exists(tmp_path):
    tool = RewriteTool(str(tmp_path))
    file_path = "test_file.txt"
    content = "Hello, world!"
    (tmp_path / file_path).write_text(content)

    with pytest.raises(ValueError) as excinfo:
        tool.write_new_file(file_path, "New content")

    assert "File already exists" in str(excinfo.value)


def test_write_new_file_failure_outside_root(tmp_path):
    tool = RewriteTool(str(tmp_path))
    file_path = "/outside_test_file.txt"

    with pytest.raises(ValueError) as excinfo:
        tool.write_new_file(file_path, "Some content")

    assert "File path must be within the root folder" in str(excinfo.value)


def test_rewrite_file_success(tmp_path):
    tool = RewriteTool(str(tmp_path))
    tool.auto_cat = False
    file_path = "test_file.txt"
    original_content = "Original content"
    (tmp_path / file_path).write_text(original_content)

    new_content = "Updated content"
    message = tool.rewrite_file(file_path, new_content)

    assert message == f"File rewritten to {tmp_path / file_path}, please view to verify contents."
    with open(tmp_path / file_path) as file:
        assert file.read() == new_content


def test_rewrite_file_failure_file_not_exists(tmp_path):
    tool = RewriteTool(str(tmp_path))
    file_path = "nonexistent_file.txt"

    with pytest.raises(FileNotFoundError) as excinfo:
        tool.rewrite_file(file_path, "Some content")

    assert "No such file or directory" in str(excinfo.value)


def test_rewrite_file_failure_outside_root(tmp_path):
    tool = RewriteTool(str(tmp_path))
    file_path = "/outside_test_file.txt"

    with pytest.raises(ValueError) as excinfo:
        tool.rewrite_file(file_path, "Some content")

    assert "File path must be within the root folder" in str(excinfo.value)
