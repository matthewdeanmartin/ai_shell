"""
An example bot that will write unit tests. The goal checker will check if pytests
are good, pass and have coverage.
"""
import asyncio
import logging
import logging.config

from dotenv import load_dotenv

import ai_shell

ai_shell.utils.logging_utils.LOGGING_ENABLED = True

with ai_shell.change_directory("src"):
    initial_passed_tests, initial_failed_tests = ai_shell.pytest_call.count_pytest_results("tests")


async def pytest_goal_checker(toolkit: ai_shell.ToolKit):
    if not toolkit:
        raise ValueError("Missing toolkit")
    pytest_stats = toolkit.get_tool_usage_for("pytest")
    if pytest_stats["count"] == 0:
        return (
            "You have not used the pytest tool yet. Please use pytest to run the tests in the tests folder."
            " Remember: read the code with cat_markdown, write tests with write_new_file, run tests with pytest."
        )
    cat_stats = toolkit.get_tool_usage_for("cat_markdown")
    if cat_stats["count"] == 0:
        return (
            "You haven't read any code-to-test, use cat_markdown to read the python file(s)."
            " Remember: read the code with cat_markdown, write tests with write_new_file, run tests with pytest."
        )
    write_new_file_stats = toolkit.get_tool_usage_for("write_new_file")
    if write_new_file_stats["count"] == 0:
        return (
            "You haven't written any tests (no usage of write_new_file)."
            " Remember: read the code with cat_markdown, write tests with write_new_file, run tests with pytest."
        )

    with ai_shell.change_directory("src"):
        passed_tests, failed_tests = ai_shell.pytest_call.count_pytest_results("tests")
    if passed_tests > initial_passed_tests and failed_tests == 0:
        return (
            f"Current pytest results : {passed_tests} passed, {failed_tests} failed, so nothing is failing and we"
            f"have more tests than when we started. "
            "Do you feel that you have written enough tests? If so, report your results using report_text."
        )
    if passed_tests == initial_passed_tests:
        return (
            f"Current pytest results : {passed_tests} passed, {failed_tests} failed, that no more passing tests than"
            f"when we started. I'd hoped for some more passing tests. "
            "Do you feel that you have written enough tests? If so, report your results using report_text."
        )
    if passed_tests == 0 and failed_tests > 0:
        return (
            f"Current pytest results : {passed_tests} passed, {failed_tests} failed, thats no passing tests and"
            f"everything is failing. We need to do better. "
            "Do you feel that you have written enough tests? If so, report your results using report_text."
        )
    return (
        f"Current pytest results : {passed_tests} passed, {failed_tests} failed "
        "Do you feel that you have written enough tests? If so, report your results using report_text."
    )


async def main():
    load_dotenv()

    logger = logging.getLogger(__name__)
    config = ai_shell.configure_logging()
    logging.config.dictConfig(config)
    logger.info("Verbose mode enabled")

    # model = "gpt-4-1106-preview" OMG this is expensive.
    model = "gpt-3.5-turbo-1106"

    bot_instructions = (
        "You are a unit test writer. You write unit tests at the bottom of code files and you use the `unittest`"
        " library and invoke the runner in an if name == main block."
    )
    tool_names = [
        # "query_todos_by_regex", "remove_todo", "add_todo",
        "ls",
        "cat_markdown",
        # "rewrite_file",
        "write_new_file",
        # "grep",
        "report_text",
        # "insert_text_after_context",
        # "insert_text_after_multiline_context",
        # "insert_text_at_start_or_end",
        # "replace_all",
        # "replace_line_by_line",
        # "replace_with_regex",
        "pytest",
    ]
    bot_name = "Unit test writer."

    dialog_logger_md = ai_shell.DialogLoggerWithMarkdown(bot_name, model, bot_instructions)
    request = """You are in the './' folder. The base folder is './'. You do not need to guess the pwd, it is './'.

The code to test is in the fish_tank folder, `./fish_tank`.  The tests are in the `./tests` folder. 

Here is a map.
fish_tank
├── __init__.py
├── __main__.py
├── README.md
tests
├── __init__.py
└── test_basic.py

Now that is out of the way, use the tools available to write pytest unit tests for each .py file in `fish_tank`
 with code, e.g. ./fish_tank/__main__.py is a good place to start. Put test files into the tests folder.

You have permission to write NEW FILES. Do not attempt to overwrite existing files.

Write tests, run tests, then report results using report_text. Then you are done.
"""
    root_folder = "e:/github/ai_shell/src"

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
    await bot.basic_tool_loop(request, root_folder, tool_names, pytest_goal_checker)
    print("Run completed.")


if __name__ == "__main__":
    asyncio.run(main())
