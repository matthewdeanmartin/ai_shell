"""
An example bot that will check if a tool works as expected.

The goal checker will check if the user has used tools that need testing.

(To be clear, this isn't the unit testing bot, that's example_test_writer_bot.py)
"""
import asyncio
import logging
import logging.config
import os

from dotenv import load_dotenv

import ai_shell

ai_shell.utils.logging_utils.LOGGING_ENABLED = True


async def main():
    load_dotenv()

    logger = logging.getLogger(__name__)
    logging.config.dictConfig(ai_shell.configure_logging())

    model = "gpt-3.5-turbo-1106"

    bot_instructions = "You are a tool tester. You will test out tools and then provide a report on if they work the way you expected them to."
    tool_names = [
        "query_todos_by_regex",
        "remove_todo",
        "add_todo",
        "ls",
        "cat_markdown",
        "rewrite_file",
        "write_new_file",
        "grep",
        "report_text",
        "insert_text_after_context",
        "insert_text_after_multiline_context",
        "insert_text_at_start_or_end",
        "replace_all",
        "replace_line_by_line",
        "replace_with_regex",
    ]
    bot_name = "cat_markdown, insert, replace tool user."

    root_folder = "src"
    if not os.path.exists(root_folder):
        raise ValueError("The demo requires that there be a src folder with some python code in it.")
    dialog_logger_md = ai_shell.DialogLoggerWithMarkdown(root_folder)
    request = """You are in the './' folder. The base folder is './'. You do not need to guess the pwd, it is './'.

Now that is out of the way, use the tools available to you to make edits to files. Then check using tools to see if 
the edits worked the way you expected them to.

Report results using report_text. Then you are done.
```
    """

    async def static_keep_going(_toolkit: ai_shell.ToolKit):
        return "Do you feel that you have exercised all the tools? If so, report your results using report_text."

    config = ai_shell.Config()
    bot = ai_shell.TaskBot(
        config,
        bot_name,
        bot_instructions,
        model,
        dialog_logger_md,
        persist_bots=True,
        persist_threads=True,
    )
    await bot.initialize()
    await bot.basic_tool_loop(request, root_folder, tool_names, static_keep_going)
    logger.info("Run completed.")


if __name__ == "__main__":
    asyncio.run(main())
