import os

import pytest

from ai_shell.cat_tool import CatTool


@pytest.fixture
def setup_test_file(tmp_path):
    # Test file content
    content = "bread\n\n\ncookies\n"

    # Create a temporary file in the temporary directory
    temp_file = tmp_path / "test_grocery_list.txt"
    temp_file.write_text(content)

    # Yield the file path for the test
    yield str(temp_file)


def test_number_lines(setup_test_file):
    absolute_file_path = os.path.abspath(setup_test_file)
    cat_tool = CatTool(root_folder=absolute_file_path)
    expected_output = "1\tbread\n2\t\n3\t\n4\tcookies\n"
    actual_output = cat_tool.cat_markdown([setup_test_file], squeeze_blank=False, number_lines=True)
    assert actual_output == expected_output


def test_squeeze_blank(setup_test_file):
    absolute_file_path = os.path.abspath(setup_test_file)
    cat_tool = CatTool(root_folder=absolute_file_path)
    expected_output = "bread\n\ncookies\n"
    actual_output = cat_tool.cat_markdown([setup_test_file], squeeze_blank=True, number_lines=False)
    assert actual_output == expected_output
