"""
This bot will attempt to add docs to the src in the `fish_tank` example.

You will need to reset the fish_tank folder to the original state after each run.
"""
import asyncio
import logging
import logging.config

from dotenv import load_dotenv
from pygount import SourceAnalysis

import ai_shell

ai_shell.utils.logging_utils.LOGGING_ENABLED = True

with ai_shell.change_directory("src"):
    initial_lines_of_code = ai_shell.count_lines_of_code("fish_tank/__main__.py")
    print(initial_lines_of_code)
    if not initial_lines_of_code.is_countable:
        raise TypeError("Can't count loc, can't continue")

def pretty_loc(loc:SourceAnalysis)->str:
    return f"Code lines: {loc.code_count}, Documentation lines:{loc.documentation_count}"

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
        # "report_text",
        "insert_text_after_context",
        "insert_text_after_multiline_context",
        "insert_text_at_start_or_end",
        "replace_all",
        "replace_line_by_line",
        "replace_with_regex",
    ]
    bot_name = "Docstring writer bot"
    language = "python"  # hack so that blacken-docs doesn't try to reformat the string contents
    request = f"""You are in the './' folder. The base folder is './'. You do not need to guess the pwd, it is './'.

Here is a map.
fish_tank
├── __init__.py
├── __main__.py
tests
├── test_import_module.py
└── __init__.py

You will add meaningful, thoughtful docstrings to the module, class, methods and functions of the `__main__.py` file.

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
files. If you use rewrite, don't omit original code!
    
```markdown
{pretty_loc(initial_lines_of_code)}
```"""

    root_folder = "e:/github/ai_shell/src"

    async def pylint_goal_checker(_toolkit: ai_shell.ToolKit):
        with ai_shell.change_directory("src"):
            lines_of_code = ai_shell.count_lines_of_code("fish_tank/__main__.py")
            if lines_of_code.documentation_count > 25 and lines_of_code.code_count >= initial_lines_of_code.code_count:
                return "DONE"
            if initial_lines_of_code.code_count < lines_of_code.code_count:
                return pretty_loc(lines_of_code) + f"\n\n Code disappeared! There used to be {initial_lines_of_code}" \
                                                   f"lines of code, now there are only {lines_of_code.code_count}! You're supposed to document not delete."
            return pretty_loc(lines_of_code) + "\n\n and thats not enough documentation. Please try again. You can do it!"

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
