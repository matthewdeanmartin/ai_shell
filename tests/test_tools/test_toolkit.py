import pytest
from openai.types.beta.threads import RequiredActionFunctionToolCall, Run
from openai.types.beta.threads.run import RequiredAction, RequiredActionSubmitToolOutputs
from openai.types.beta.threads.runs.function_tool_call import Function

from ai_shell.openai_toolkit import ToolKit
from ai_shell.openai_tools import just_tool_names

pytestmark = pytest.mark.anyio


def test_grep():
    kit = ToolKit(".", "gpt-3.5-turbo", 500, just_tool_names())
    result = kit.grep({"glob_pattern": "**/*.py", "regex": "test_grep", "maximum_matches": 1})
    assert result.data


async def test_tk():
    names = just_tool_names()
    kit = ToolKit("tests", "gpt-3.5-turbo", 500, names)
    run = Run(
        id="123",
        assistant_id="123",
        created_at="123",
        expires_at="123",
        file_ids=["123"],
        instructions="123",
        object="thread.run",
        model="123",
        status="queued",
        thread_id="123",
        tools=[],
        required_action=RequiredAction(
            type="submit_tool_outputs",
            submit_tool_outputs=RequiredActionSubmitToolOutputs(
                tool_calls=[
                    RequiredActionFunctionToolCall(
                        id="123",
                        type="function",
                        function=Function(name=name, arguments="{}"),
                    )
                    for name in names
                    if not name.startswith("pytest")
                ]
            ),
        ),
    )

    result = await kit.process_tool_calls(run)
    assert result
