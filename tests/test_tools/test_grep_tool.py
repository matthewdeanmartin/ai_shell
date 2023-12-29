import os
import tempfile

import pytest

from ai_shell.grep_tool import GrepTool  # Make sure to import your GrepTool class correctly
from ai_shell.utils.read_fs import temporary_change_dir
from tests.util import config_for_tests


@pytest.fixture
def temp_file_with_content():
    """Fixture to create a temporary file with specific content."""
    content = '# comment\nprint("Hello World")\n'
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write(content)
        tmp.flush()
        yield tmp.name  # This yields the path to the temporary file


def test_grep_comment_lines(temp_file_with_content):
    with temporary_change_dir(str(temp_file_with_content)):
        absolute_file_path = os.path.abspath(temp_file_with_content)
        grep_tool = GrepTool(root_folder=absolute_file_path, config=config_for_tests())
        regex = "^#.*"  # Regex pattern for lines starting with '#'
        glob_pattern = temp_file_with_content  # Use the path of the temporary file
        results = grep_tool.grep(regex, glob_pattern)
        assert len(results.data) == 1
        assert len(results.data[0].found) == 1
        assert results.data[0].found[0].line == "# comment"


def test_grep_print_lines(temp_file_with_content):
    with temporary_change_dir(str(temp_file_with_content)):
        absolute_file_path = os.path.abspath(temp_file_with_content)
        grep_tool = GrepTool(root_folder=absolute_file_path, config=config_for_tests())
        regex = r"print\(.*\)"  # Regex pattern for lines with 'print'
        glob_pattern = temp_file_with_content  # Use the path of the temporary file
        results = grep_tool.grep(regex, glob_pattern)
        assert len(results.data) == 1
        assert len(results.data[0].found) == 1
        assert results.data[0].found[0].line == 'print("Hello World")'


def test_grep_print_lines_markdown(temp_file_with_content):
    with temporary_change_dir(str(temp_file_with_content)):
        absolute_file_path = os.path.abspath(temp_file_with_content)
        grep_tool = GrepTool(root_folder=absolute_file_path, config=config_for_tests())
        regex = r"print\(.*\)"  # Regex pattern for lines with 'print'
        glob_pattern = temp_file_with_content  # Use the path of the temporary file
        results = grep_tool.grep_markdown(regex, glob_pattern).split("\n")
        results_string = "\n".join(results[1:])
        assert results_string == 'line 2: print("Hello World")\n1 matches found and 1 displayed. Skipped -1\n'
