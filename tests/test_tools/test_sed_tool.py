# Unit tests for each scenario
from ai_shell.sed_tool import SedTool
from tests.util import config_for_tests


def test_regex_substitution():
    input_text = "Hello World\nThis is a test"
    commands = ["s/World/Universe/"]
    expected_output = "Hello Universe\nThis is a test"
    tool = SedTool(".", config=config_for_tests())
    assert tool._process_sed(input_text, commands) == expected_output


def test_print():
    input_text = "Hello World\nThis is a test"
    commands = ["p"]
    expected_output = input_text  # 'p' should print each line as it is
    tool = SedTool(".", config=config_for_tests())
    assert tool._process_sed(input_text, commands) == expected_output


def test_append():
    input_text = "Hello World"
    commands = ["a\\Appended text"]
    expected_output = "Hello World\nAppended text"
    tool = SedTool(".", config=config_for_tests())
    assert tool._process_sed(input_text, commands) == expected_output


def test_insert():
    input_text = "Hello World"
    commands = ["i\\Inserted text"]
    expected_output = "Inserted text\nHello World"
    tool = SedTool(".", config=config_for_tests())
    assert tool._process_sed(input_text, commands) == expected_output


def test_change():
    input_text = "Hello World\nThis is a test"
    commands = ["2c\\Changed line"]
    expected_output = "Hello World\nChanged line"
    tool = SedTool(".", config=config_for_tests())
    assert tool._process_sed(input_text, commands) == expected_output
