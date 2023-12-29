"""
An example bot that will write unit tests. The goal checker will check if pytests
are good, pass and have coverage.
"""
import asyncio
import logging
import logging.config
import os

from dotenv import load_dotenv

import ai_shell
import ai_shell.externals.pytest_call

ai_shell.utils.logging_utils.LOGGING_ENABLED = True

initial_passed_tests = -1
initial_failed_tests = -1
initial_coverage = -1.0
initial_pytest_output = None

if __name__ == "__main__":
    with ai_shell.change_directory("src"):
        (
            initial_passed_tests,
            initial_failed_tests,
            initial_coverage,
            initial_pytest_output,
        ) = ai_shell.externals.pytest_call.count_pytest_results("fish_tank", "tests", 80)


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
        passed_tests, failed_tests, coverage, pytest_output = ai_shell.externals.pytest_call.count_pytest_results(
            "fish_tank", "tests", 80
        )
    if coverage >= 80:
        return "DONE"
    if passed_tests > initial_passed_tests and initial_coverage == coverage:
        return (
            "You've written more tests, but coverage didn't go up. Was that a meaningful test? Try harder. "
            "We are counting on you."
        )

    message = (
        f"Current pytest results : {passed_tests} passed, {failed_tests} failed, coverage {coverage}%\n\n"
        + pytest_output.stdout
        + "\n\n"
    )
    # if passed_tests > initial_passed_tests and failed_tests == 0:
    #     return (
    #         f"{message}\n"
    #         f"So nothing is failing and we "
    #         f"have more tests than when we started. "
    #     )
    if passed_tests == initial_passed_tests:
        return (
            f"{message}\n"
            " That's no more passing tests than "
            f"when we started. I'd hoped for some more passing tests. Keep writing tests, please."
        )
    if passed_tests == 0 and failed_tests > 0:
        return (
            f"{message}\n"
            f"That's no passing tests and "
            f"everything is failing. We need to do better. Keep writing tests, please."
        )

    return (
        f"{message}\n"
        f"Current pytest results : {passed_tests} passed, {failed_tests} failed. Keep writing tests, please."
    )


async def main():
    load_dotenv()

    logger = logging.getLogger(__name__)

    logging.config.dictConfig(ai_shell.configure_logging())
    logger.info("Verbose mode enabled")

    # model = "gpt-4-1106-preview" OMG this is expensive.
    model = "gpt-3.5-turbo-1106"

    bot_instructions = (
        "You are a unit test writer. You write pytest style unit tests in the tests folder and you use the `pytest`"
        " tool, write_new_file tool, cat_markdown tool and report_text tool to accomplish your goal."
    )
    tool_names = [
        # "query_todos_by_regex", "remove_todo", "add_todo",
        "ls",
        "cat_markdown",
        "rewrite_file",
        "write_new_file",
        # "grep",
        # "report_text", # Don't let it self-certify.
        # "insert_text_after_context",
        # "insert_text_after_multiline_context",
        # "insert_text_at_start_or_end",
        # "replace_all",
        # "replace_line_by_line",
        # "replace_with_regex",
        "pytest",
    ]
    bot_name = "Unit test writer."

    dialog_logger_md = ai_shell.DialogLoggerWithMarkdown("./logs/dialogs/")
    request = """We have an important task. You are the best unit test writer we have. We are counting
on you to get this right.

You are in the './' folder. The base folder is './'. You do not need to guess the pwd, it is './'.

The code to test is in the fish_tank folder, `./fish_tank`.  The tests are in the `./tests` folder. 

Here is a map.
fish_tank
├── __init__.py
├── __main__.py
tests
├── test_import_module.py
└── __init__.py

Do not start writing tests until you use cat_markdown tool to read the fish_tank code.

Now that is out of the way, use the tools available to write pytest unit tests for each .py file in `fish_tank`
 with code, e.g. ./fish_tank/__main__.py is a good place to start. Put test files into the tests folder.

You have permission to write new files with write_new_file. 

You have permission to rewrite entire files with the rewrite_file tool.

Tests should meaningfully exercise the code in the fish_tank folder and achieve 80% coverage.

- Do not write unit tests with out assertions. 
- Do not write unit tests with `pass` as the body.
- Do not add new functions to fish_tank module just to test them, test only pre-existing functions.

Write tests, run tests. You are done when the coverage is 80% or more.
"""
    root_folder = "src"
    if not os.path.exists(root_folder):
        raise ValueError("The demo requires that there be a src folder with some python code in it.")

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
