from ai_shell.openai_toolkit import ToolKit
from ai_shell.openai_tools import just_tool_names


def test_grep():
    kit = ToolKit(".", "gpt-3.5-turbo", 500, just_tool_names())
    result = kit.grep({"glob_pattern": "**/*.py", "regex": "test_grep", "maximum_matches": 1})
    assert result.data
