from ai_shell.replace_tool import ReplaceTool


def test_replacement_in_single_line(tmp_path):
    file_path = tmp_path / "dummy.txt"
    file_path.write_text("Hello World")
    tool = ReplaceTool(str(tmp_path))
    tool.auto_cat = False
    result = tool.replace_line_by_line(str(file_path), "World", "Universe")
    assert result == "Changes applied without exception, please verify by other means."
    assert file_path.read_text() == "Hello Universe"


def test_replacement_in_multiple_lines(tmp_path):
    file_path = tmp_path / "dummy.txt"
    file_path.write_text("Hello\nWorld")
    tool = ReplaceTool(str(tmp_path))
    tool.auto_cat = False
    result = tool.replace_line_by_line(str(file_path), "World", "Universe", 1 - 1, 2)
    assert result == "Changes applied without exception, please verify by other means."
    assert file_path.read_text() == "Hello\nUniverse"


def test_no_replacement_needed(tmp_path):
    file_path = tmp_path / "dummy.txt"
    file_path.write_text("Hello World")
    tool = ReplaceTool(str(tmp_path))
    result = tool.replace_line_by_line(str(file_path), "Universe", "Galaxy")
    assert (
        result
        == "No changes made, this means the old file contents are the same as the new. This has nothing to do with file permissions. Try again with a different match pattern."
    )
    assert file_path.read_text() == "Hello World"


def test_replace_all_occurrences(tmp_path):
    file_path = tmp_path / "dummy.txt"
    file_path.write_text("Hello World World")
    tool = ReplaceTool(str(tmp_path))
    tool.auto_cat = False
    result = tool.replace_all(str(file_path), "World", "Universe")
    assert result == "Changes applied without exception, please verify by other means."
    assert file_path.read_text() == "Hello Universe Universe"


def test_replace_with_regex(tmp_path):
    file_path = tmp_path / "dummy.txt"

    file_path.write_text("Hello World123")
    file_path.read_text()
    tool = ReplaceTool(str(tmp_path))
    tool.auto_cat = False
    result = tool.replace_with_regex(str(file_path), regex_match_expression="\\bWorld[0-9]+\\b", replacement="")
    assert result == "Changes applied without exception, please verify by other means."
    assert file_path.read_text() == "Hello "
