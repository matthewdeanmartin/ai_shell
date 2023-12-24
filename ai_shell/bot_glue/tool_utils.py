import logging
import time

from ai_shell.openai_toolkit import ToolKit

logger = logging.getLogger(__name__)


async def loop_tools(client, kit: ToolKit, run, thread, dialog_logger_md) -> int:
    waiting = False
    tool_use_count = 0
    while True:
        if run.status in ("queued", "in_progress"):
            print(".", end="")
            waiting = True
            time.sleep(1)
        elif run.status in ("failed", "cancelling", "cancelled", "expired"):
            raise Exception(run.last_error)
        elif run.status == "completed":
            logger.info("completed")
            if waiting:
                print()
            break
        elif run.status == "requires_action":
            logger.info("requires_action")
            if waiting:
                print()
                waiting = False
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                tool_use_count += 1
                dialog_logger_md.add_tool(tool_call.function.name, tool_call.function.arguments)
            results = await kit.process_tool_calls(run, print)
            dialog_logger_md.add_tool_result(results)
            # submit results
            run = await client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=results,
            )
            run = await client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            continue
        else:
            raise Exception(run.status)
        # poll
        run = await client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    return tool_use_count
