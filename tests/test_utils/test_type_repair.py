import pytest

from ai_shell.utils.type_repair import convert_to_list


def test_convert_single_item_string():
    assert convert_to_list("simple.py") == ["simple.py"], "Failed to convert single item string"


def test_convert_csv_string():
    assert convert_to_list('"foo.py, bar.py", example.py') == [
        "foo.py, bar.py",
        " example.py",
    ], "Failed to handle CSV string"


def test_convert_list():
    assert convert_to_list(["already", "a", "list"]) == ["already", "a", "list"], "Failed to return an existing list"


def test_convert_empty_string():
    assert convert_to_list("") == [], "Failed to handle empty string"


def test_convert_non_list_non_string():
    with pytest.raises(TypeError):
        convert_to_list(None)
