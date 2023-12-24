import os

import pytest

from ai_shell.cut_tool import CutTool, is_in_ranges, parse_ranges


@pytest.mark.parametrize(
    "index, ranges, expected",
    [
        (1, [1, 2, 3], True),
        (4, [(1, 3), 5], False),
        (5, [(1, 3), 5], True),
        (2, [(1, 5)], True),
        (6, [(1, 5)], False),
        (1, [(2, 4)], False),
        (3, [(2, 4), 7], True),
        (7, [(2, 4), 7], True),
        (8, [(2, 4), (6, 7)], False),
        (1, [], False),
    ],
)
def test_is_in_ranges(index, ranges, expected):
    assert is_in_ranges(index, ranges) == expected


def create_test_file(tmp_path):
    # Create a temporary CSV file
    test_file = tmp_path / "test.csv"
    with open(test_file, "w") as f:
        f.write("Field1,Field2,Field3\n")
        f.write("A,B,C\n")
        f.write("D,E,F\n")

    # Yield the file path for the test
    return str(test_file)


def test_parse_ranges():
    # Example usage:
    assert parse_ranges("1-5,10") == [(1, 5), 10]

    assert parse_ranges("2,3-4") == [2, (3, 4)]


def test_cut_fields_by_name(tmp_path):
    path = create_test_file(tmp_path)
    absolute_file_path = os.path.abspath(path)
    # Call the function with the temporary file and assert its output
    expected_output = "B\nE\n"
    tool = CutTool(root_folder=str(absolute_file_path))
    actual_output = tool.cut_fields_by_name(str(absolute_file_path), ["Field2"])
    assert actual_output == expected_output


def test_cut_fields_by_index(tmp_path):
    path = create_test_file(tmp_path)
    absolute_file_path = os.path.abspath(path)
    # Call the function with the temporary file and assert its output
    expected_output = "Field1,Field2\nA,B\nD,E\n"
    tool = CutTool(root_folder=str(absolute_file_path))
    actual_output = tool.cut_fields(str(absolute_file_path), "1,2")
    assert actual_output == expected_output


def test_cut_chars_by_range(tmp_path):
    path = create_test_file(tmp_path)
    absolute_file_path = os.path.abspath(path)
    # Call the function with the temporary file and assert its output
    expected_output = "Fed\nABC\nDEF\n"
    tool = CutTool(root_folder=str(absolute_file_path))
    actual_output = tool.cut_characters(str(absolute_file_path), "1-1,3-3,5-5")
    assert actual_output == expected_output
