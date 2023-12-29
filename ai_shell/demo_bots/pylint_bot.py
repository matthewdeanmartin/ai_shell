"""
This bot will attempt to lint the issues in the `fish_tank` example.

You will need to reset the fish_tank folder to the original state after each run.
"""

import asyncio
import logging
import logging.config
import os

from dotenv import load_dotenv

import ai_shell
import ai_shell.demo_bots.demo_setup as demo_setup

ai_shell.utils.logging_utils.LOGGING_ENABLED = True

if __name__ == "__main__" and not os.path.exists("src"):
    demo_setup.initialize()


initial_pylint = None
if __name__ == "__main__":
    with ai_shell.change_directory("src"):
        initial_pylint = ai_shell.invoke_pylint("fish_tank", 8)

        if initial_pylint.return_code == 0:
            raise ValueError("The pylint score is already high enough. Bot won't have any work to do.")


async def main():
    load_dotenv()

    logger = logging.getLogger(__name__)
    logging.config.dictConfig(ai_shell.configure_logging())
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
    language = "python"  # hack so that blacken-docs doesn't try to reformat the string contents
    if not initial_pylint:
        raise ValueError("Pylint data must be initialized.")
    request = f"""You are in the './' folder. The base folder is './'. You do not need to guess the pwd, it is './'.

Here is a map.
fish_tank
├── __init__.py
├── __main__.py
tests
├── test_import_module.py
└── __init__.py

Do not start addressing pylint issues until you use cat_markdown tool to read the fish_tank code.

- Don't even think of modifying a file with running cat_markdown first.
- Do not attempt to address linting issues by adding arbitrary code.
- Do not add functions with empty bodies or `pass` 

If you use the rewrite_file tool, it will blow away any previous contents. Please don't accidentally delete code.

This is an example of google style doc strings.
```{language}
def create_fish(emoji: str, x: int, y: int) -> None:
    \"\"\"
    Create a fish.
    Args:
        emoji (str): The emoji to use for the fish.
        x (int): The starting x coordinate.
        y (int): The starting y coordinate.
    \"\"\"
```        

Now that is out of the way, use the rewrite tool (and/or other tool) to add google style docstrings to the fish_tank 
files. As you can see, pylint says they're missing. After each round of edits, you'll see the updated output of pylint.
    
```markdown
{initial_pylint.to_markdown()}
```"""

    root_folder = "src"
    if not os.path.exists(root_folder):
        raise ValueError("The demo requires that there be a src folder with some python code in it.")

    async def pylint_goal_checker(_toolkit: ai_shell.ToolKit):
        # already in src!
        result = ai_shell.invoke_pylint("fish_tank", 8)
        if result.return_code == 0:
            return "DONE"
        return result.to_markdown() + "\n\nThe pylint score is too low. Please try again. You can do it!"

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
    with ai_shell.change_directory("src"):
        await bot.initialize()
        await bot.basic_tool_loop(request, root_folder, tool_names, pylint_goal_checker)
        logger.info("Run completed.")


if __name__ == "__main__":
    asyncio.run(main())
