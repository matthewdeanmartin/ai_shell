import pytest

from ai_shell.openai_toolkit import ToolKit
from ai_shell.openai_tools import just_tool_names
from tests.util import config_for_tests

pytestmark = pytest.mark.anyio


def test_grep():
    kit = ToolKit(".", "gpt-4o-mini", 500, just_tool_names(), config=config_for_tests())
    result = kit.grep({"glob_pattern": "**/*.py", "regex": "test_grep", "maximum_matches": 1})
    assert result.data


# async def test_tk():
#     # Get the directory of the current script
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#
#     # Get the parent directory
#     parent_dir = os.path.dirname(script_dir)
#
#     parent_dir = os.path.dirname(parent_dir)
#     # Change the current working directory to the parent directory
#     with temporary_change_dir(parent_dir):
#         names = just_tool_names()
#         kit = ToolKit("tests", "gpt-4o-mini", 500, names, config=config_for_tests())
#         run = Run(
#             id="123",
#             assistant_id="123",
#             created_at="123",
#             expires_at="123",
#             file_ids=["123"],
#             instructions="123",
#             object="thread.run",
#             model="123",
#             status="queued",
#             thread_id="123",
#             tools=[],
#             required_action=RequiredAction(
#                 type="submit_tool_outputs",
#                 submit_tool_outputs=RequiredActionSubmitToolOutputs(
#                     tool_calls=[
#                         RequiredActionFunctionToolCall(
#                             id="123",
#                             type="function",
#                             function=Function(name=name, arguments="{}"),
#                         )
#                         for name in names
#                         if not name.startswith("pytest")
#                     ]
#                 ),
#             ),
#         )
#
#         result = await kit.process_tool_calls(run)
#         assert result
#
#
# async def test_tk_markdown():
#     # Get the directory of the current script
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#
#     # Get the parent directory
#     parent_dir = os.path.dirname(script_dir)
#
#     parent_dir = os.path.dirname(parent_dir)
#
#     markdown_tools = []
#     all_names = just_tool_names()
#     for tool in all_names:
#         if tool.endswith("_markdown"):
#             match = tool[: -len("_markdown")]
#             if match in all_names:
#                 markdown_tools.append(match)
#             else:
#                 print(f"Markdown tool {tool} has no match!!")
#
#     # Change the current working directory to the parent directory
#     with temporary_change_dir(parent_dir):
#         names = markdown_tools
#         kit = ToolKit("tests", "gpt-4o-mini", 500, names, config=config_for_tests())
#         run = Run(
#             id="123",
#             assistant_id="123",
#             created_at="123",
#             expires_at="123",
#             file_ids=["123"],
#             instructions="123",
#             object="thread.run",
#             model="123",
#             status="queued",
#             thread_id="123",
#             tools=[],
#             required_action=RequiredAction(
#                 type="submit_tool_outputs",
#                 submit_tool_outputs=RequiredActionSubmitToolOutputs(
#                     tool_calls=[
#                         RequiredActionFunctionToolCall(
#                             id="123",
#                             type="function",
#                             function=Function(name=name, arguments="{'mime_type': 'text/markdown'}"),
#                         )
#                         for name in names
#                         if not name.startswith("pytest")
#                     ]
#                 ),
#             ),
#         )
#
#         result = await kit.process_tool_calls(run)
#         assert result
