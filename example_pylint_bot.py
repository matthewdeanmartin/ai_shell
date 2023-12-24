"""
This bot will attempt to lint the issues in the `fish_tank` example.

You will need to reset the fish_tank folder to the original state after each run.
"""
import asyncio
import logging
import logging.config

from dotenv import load_dotenv

import ai_shell

ai_shell.utils.logging_utils.LOGGING_ENABLED = True


async def main():
    load_dotenv()

    logger = logging.getLogger(__name__)
    config = ai_shell.configure_logging()
    logging.config.dictConfig(config)
    model = "gpt-3.5-turbo-1106"

    # The bot likes praise.
    bot_instructions = (
        "You are a persistent, excellent python developer. You think about your code and reason in steps."
    )
    # Too many tools will confuse the bot.
    tool_names = [
        "ls",
        "cat_markdown",
        "rewrite_file",
        "write_new_file",
        "report_text",
        "insert_text_after_context",
        "insert_text_after_multiline_context",
        "insert_text_at_start_or_end",
        "replace_all",
        "replace_line_by_line",
        "replace_with_regex",
    ]
    bot_name = "Pylint fixer bot"

    request = f"""You are in the './' folder. The base folder is './'. You do not need to guess the pwd, it is './'.

Now that is out of the way, use the rewrite tool (and/or other toolkit_factory) to add google style docstrings to the fish_tank files. As you
can see, pylint says they're missing. After each round of edits, you'll see the updated output of pylint.
    
```{ai_shell.invoke_pylint("fish_tank")}
```
    """

    root_folder = "e:/github/ai_shell/src"

    def pylint_goal_checker(_toolkit: ai_shell.ToolKit):
        return (
            ai_shell.invoke_pylint("fish_tank") + "\n\nIf you are not done, keep using toolkit_factory. "
            "If you are done, or find the task impossible, or something else, "
            "submit your final report to the report_text tool, with an answer of"
            " 'DONE' or 'IMPOSSIBLE', just one word. If you need to submit some "
            "additional explanations, put it in the comment."
        )

    config = ai_shell.Config()
    bot = ai_shell.TaskBot(
        config,
        bot_name,
        bot_instructions,
        model,
        ai_shell.DialogLoggerWithMarkdown("./tmp"),
        persist_bots=True,
        persist_threads=True,
    )
    await bot.initialize()
    await bot.basic_tool_loop(request, root_folder, tool_names, pylint_goal_checker)
    logger.info("Run completed.")


if __name__ == "__main__":
    asyncio.run(main())
