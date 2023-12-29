import pytest

from ai_shell import HeadTailTool
from tests.util import config_for_tests


def create_test_file(tmp_path, content, binary=False):
    test_file = tmp_path / "test.txt"
    mode = "wb" if binary else "w"
    with test_file.open(mode) as f:
        if binary:
            f.write(content.encode("utf-8"))  # Write bytes for binary content
        else:
            f.write(content)
    return test_file


@pytest.fixture
def tool(tmp_path):
    # Set up HeadTailTool with the temporary path
    return HeadTailTool(root_folder=str(tmp_path), config=config_for_tests())


def test_head(tool, tmp_path):
    content = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
    test_file = create_test_file(tmp_path, content)

    expected_output = ["Line 1", "Line 2", "Line 3"]
    assert tool.head(str(test_file), 3) == expected_output


def test_tail(tool, tmp_path):
    content = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
    test_file = create_test_file(tmp_path, content)

    expected_output = ["Line 3", "Line 4", "Line 5"]
    assert tool.tail(str(test_file), 3) == expected_output


def test_head_bytes(tool, tmp_path):
    content = "12345\n67890\nabcde"
    test_file = create_test_file(tmp_path, content, binary=True)

    expected_output = ["12345\n"]
    assert tool.head(str(test_file), byte_count=6) == expected_output


def test_tail_bytes(tool, tmp_path):
    content = "12345\n67890\nabcde"
    test_file = create_test_file(tmp_path, content, binary=True)

    expected_output = ["abcde"]
    assert tool.tail(str(test_file), byte_count=5) == expected_output
