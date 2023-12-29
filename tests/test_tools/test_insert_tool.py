import pytest

from ai_shell.insert_tool import InsertTool
from tests.util import config_for_tests


def create_sample_file(tmp_path, content):
    file_path = tmp_path / "sample.txt"
    with open(file_path, "w") as file:
        file.writelines(content)
    return file_path


def test_insert_text_after_context_positive(tmp_path):
    tool = InsertTool(str(tmp_path), config=config_for_tests())
    file_path = create_sample_file(tmp_path, ["Line 1\n", "Context Line\n", "Line 3\n"])
    tool.insert_text_after_context(str(file_path), "Context Line", "Inserted Text")

    with open(file_path) as file:
        lines = file.readlines()

    assert "Inserted Text\n" in lines
    assert lines.index("Inserted Text\n") == 2


def test_insert_text_after_context_negative(tmp_path):
    tool = InsertTool(str(tmp_path), config=config_for_tests())
    file_path = create_sample_file(tmp_path, ["Line 1\n", "Line 2\n", "Line 3\n"])

    with pytest.raises(ValueError):
        tool.insert_text_after_context(str(file_path), "Non-existent Context", "Inserted Text")


@pytest.mark.parametrize("position", ["start", "end"])
def test_insert_text_at_position_positive(tmp_path, position):
    tool = InsertTool(str(tmp_path), config=config_for_tests())
    file_path = create_sample_file(tmp_path, ["Line 1\n", "Line 2\n", "Line 3\n"])
    tool.insert_text_at_start_or_end(str(file_path), "Inserted Text", position)

    with open(file_path) as file:
        lines = file.readlines()

    if position == "start":
        assert lines[0] == "Inserted Text\n"
    else:
        assert lines[-1] == "Inserted Text\n"


def test_insert_text_at_position_negative(tmp_path):
    tool = InsertTool(str(tmp_path), config=config_for_tests())
    file_path = create_sample_file(tmp_path, ["Line 1\n", "Line 2\n", "Line 3\n"])

    with pytest.raises(ValueError):
        tool.insert_text_at_start_or_end(str(file_path), "Inserted Text", "middle")


def test_insert_text_after_multiline_context_positive(tmp_path):
    tool = InsertTool(str(tmp_path), config=config_for_tests())
    file_path = create_sample_file(tmp_path, ["Line 1\n", "Context Line 1\n", "Context Line 2\n", "Line 4\n"])
    context_lines = ["Context Line 1", "Context Line 2"]
    tool.insert_text_after_multiline_context(str(file_path), context_lines, "Inserted Text")

    with open(file_path) as file:
        file_string = file.read()

    assert "Line 1\nContext Line 1\nContext Line 2\nInserted Text\nLine 4\n" in file_string


def test_insert_text_after_multiline_context_negative(tmp_path):
    tool = InsertTool(str(tmp_path), config=config_for_tests())
    file_path = create_sample_file(tmp_path, ["Line 1\n", "Line 2\n", "Line 3\n"])
    context_lines = ["Non-existent Context Line 1", "Non-existent Context Line 2"]

    with pytest.raises(ValueError):
        tool.insert_text_after_multiline_context(str(file_path), context_lines, "Inserted Text")
