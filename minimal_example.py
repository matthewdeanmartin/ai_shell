"""
Try to set up absolute minimum for a tool call.
"""
import asyncio
import logging.config
import time

from dotenv import load_dotenv
from openai import AsyncOpenAI

import ai_shell
import ai_shell.utils.logging_utils
from ai_shell.utils.log_conversation import DialogLoggerWithMarkdown

ai_shell.utils.logging_utils.LOGGING_ENABLED = True

load_dotenv()

logger = logging.getLogger("ai_shell")
config = ai_shell.configure_logging()
logging.config.dictConfig(config)
logger.info("Verbose mode enabled")

# model = "gpt-4-1106-preview" OMG this is expensive.
model = "gpt-3.5-turbo-1106"
bot_name = "ls, insert, replace, cat, grep tool user."
bot_instructions = (
    "You are a persistent, excellent python developer. You think about your code and reason in steps."
    # "You will find the TODOs in the source code, then record them with the TODO"
    # " tool. Write the todo items into the todo tool."
)

dialog_logger_md = DialogLoggerWithMarkdown(bot_name, model, bot_instructions)
request = (
    "Please use ls to list the available files. Then use grep to find the TODO items. Then record the TODO items in the todo tool."
    " Then write code to accomplish the task indicated by the TODO, to edit the source code as found with the ls tool using sed to edit the files."
    " Just to be clear, I want you to do what the TODO requests, don't just change the text of the TODO comment."
)
request = "Look at __main__.py cat_markdown, read and understand the code. Now add emoji waves to the top line of the simulated fish tank(the buffer in init and update()), so when fish tank runs, the user will see waves at the top of the screen. Using the toolkit_factory for insert and or replace as appropriate. Edit self.buffer's initialization code!"
main_goal = "and self.buffer is initialized so the 1st row is a row of WATER wave emojis AND same for update() and really the update to the buffer in update is more important as the screen redraws every half second..."
dialog_logger_md.add_user(request)
tool_names = [
    # "query_todos_by_regex", "remove_todo", "add_todo",
    "ls",
    "cat_markdown",
    "grep",
    # "sed"
    "insert_text_after_context",
    "insert_text_after_multiline_context",
    "insert_text_at_start_or_end",
    "replace_all",
    "replace_line_by_line",
    "replace_with_regex",
]
dialog_logger_md.add_toolkit(tool_names)
root_folder = "e:/github/ai_shell/fish_tank"

keep_going = (
    f"Continue to use toolkit_factory to accomplish the mission. "
    f"If you've edited code, `cat` it and look to see if you've introduced any bugs. "
    f"If you are done, {main_goal}, reply with one word, 'DONE'."
)


async def main():
    load_dotenv()
    thread = None
    assistant = None
    try:
        kit = ai_shell.ToolKit(root_folder, model, 500)
        # minimal Assistant + tool call
        client = AsyncOpenAI()
        ai_shell.initialize_all_tools(keeps=tool_names)

        tools = [{"function": schema, "type": "function"} for schema in ai_shell.ALL_TOOLS]
        if not tools:
            raise Exception("Not enough toolkit_factory!")
        assistant_id = ""
        if not assistant_id:
            assistant = await client.beta.assistants.create(
                name=bot_name,
                instructions=bot_instructions,
                # model="gpt-3.5-turbo-0613", # "gpt-3.5-turbo",  # Cheap and smart enough
                model=model,
                tools=tools,
            )
        else:
            assistant = await client.beta.assistants.retrieve(assistant_id)
        logger.debug(f"Assistant id: {assistant.id}")
        thread = await client.beta.threads.create()
        # print(thread)

        logger.info(request)
        await client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=request,
        )
        # logger.info(message)
        run = await client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
        done = "NOPE"
        while done != "DONE":
            await loop_tools(client, kit, run, thread)

            messages = await client.beta.threads.messages.list(thread_id=thread.id, order="desc")
            # logger.info(messages)
            done = capture_message(done, messages)
            if done == "DONE":
                dialog_logger_md.add_bot(done)
            elif done != "DONE":
                # TODO: 2nd bot should do this.
                print(keep_going)
                dialog_logger_md.add_user(keep_going)
                logger.info(keep_going)
                await client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=keep_going,
                )
                run = await client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

    except Exception as exception:
        dialog_logger_md.add_error(exception)
    finally:
        # clean up thread
        if thread:
            await client.beta.threads.delete(thread.id)
        if assistant:
            # clean up assistant
            await client.beta.assistants.delete(assistant.id)
        raise


def capture_message(done, messages):
    for key, message in messages:
        if key == "data":
            text_message = message[0].content[0].text.value
            print(text_message)
            dialog_logger_md.add_bot(text_message)
            logger.info(text_message)
            if "DONE" in str(text_message).upper():
                done = "DONE"
                break
    return done


async def loop_tools(client, kit, run, thread):
    waiting = False
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


if __name__ == "__main__":
    # Python 3.7+
    asyncio.run(main())
