import pytest

from ai_shell.pycat_tool import PyCatTool, format_path_as_header, is_python_file, read_file_contents


def test_is_python_file():
    assert is_python_file("example.py") is True
    assert is_python_file("example.txt") is False
    assert is_python_file("example") is False


def test_format_path_as_header():
    assert format_path_as_header("path/to/file.py") == "## path/to/file.py\n\n"
    assert format_path_as_header("") == "## \n\n"


def test_read_file_contents(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Sample content")
    assert read_file_contents(str(file_path)) == "Sample content"
    # Add more tests, including error handling


def create_test_files(directory, files_content):
    for file_name, content in files_content.items():
        (directory / file_name).write_text(content)


@pytest.fixture
def python_files(tmp_path):
    files_content = {"script1.py": "print('Hello, world!')\n", "script2.py": "def foo():\n    return 'bar'\n"}
    create_test_files(tmp_path, files_content)
    return tmp_path, files_content


def test_format_code_with_python_files(python_files, tmp_path):
    base_path, files_content = python_files

    tool = PyCatTool(str(base_path))
    content = tool.format_code_as_markdown(str(base_path), header="Test Header")

    # Check for header
    assert "# Test Header Source Code\n\n" in content

    # Check for file content
    for file_name, file_content in files_content.items():
        assert f"## {file_name}\n\n```python\n{file_content}\n```\n\n" in content


def test_format_code_empty_directory(python_files, tmp_path):
    base_path, files_content = python_files
    tool = PyCatTool(str(base_path))
    content = tool.format_code_as_markdown(str(tmp_path), header="Empty Dir Header")

    assert "# Empty Dir Header Source Code\n\n" in content
    # Additional checks can be added to ensure no file content is included


def test_format_code_with_tree_header(python_files, tmp_path):
    base_path, _ = python_files
    tool = PyCatTool(str(base_path))
    content = tool.format_code_as_markdown(str(base_path), header="tree")

    assert "# Source Code Filesystem Tree\n\n" in content
    # Additional checks can be added to ensure tree structure is included correctly
