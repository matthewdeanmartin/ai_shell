"""
An example bot that will write unit tests. The goal checker will check if pytests
are good, pass and have coverage.
"""

import asyncio
import logging
import logging.config
import os
from importlib.resources import files

from dotenv import load_dotenv

import ai_shell
import ai_shell.demo_bots.demo_setup as demo_setup
import ai_shell.externals.pytest_call
import ai_todo

ai_shell.ai_logs.log_to_bash.LOGGING_ENABLED = True

if __name__ == "__main__" and not os.path.exists("src"):
    demo_setup.initialize()

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

    # host script must set pwd.
    passed_tests, failed_tests, coverage, pytest_output = ai_shell.externals.pytest_call.count_pytest_results(
        "fish_tank", "tests", 80
    )
    if coverage >= 80:
        return toolkit.conversation_over_marker
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

    short_name = "todo"
    source = files("ai_shell").joinpath(f"demo_bots/{short_name}_bot_instructions.md")
    with open(str(source), encoding="utf-8") as instructions:
        bot_instructions = instructions.read()
    tool_names = [
        # "query_todos_by_regex", "remove_todo", "add_todo",
        "ls",
        "cat_markdown",
        # "rewrite_file", It keeps trying to use this for insert, wrecking the file, getting caught & giving up.
        "write_new_file",
        # "grep",
        "report_text",  # Don't let it self-certify.
        # "insert_text_after_context",
        # "insert_text_after_multiline_context",
        # "insert_text_at_start_or_end",
        # "replace_all",
        # "replace_line_by_line",
        # "replace_with_regex",
        "pytest",
    ]
    bot_name = "Pytest Unit test writer."

    dialog_logger_md = ai_shell.DialogLoggerWithMarkdown("./tmp")
    source = files("ai_shell").joinpath(f"demo_bots/{short_name}_bot_mission.md")
    with open(str(source), encoding="utf-8") as instructions:
        request = instructions.read()
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
    if not config.get_list("todo_roles"):
        config.set_list("todo_roles", ["Developer", "Tester"])
    ai_todo.TaskManager("src", config.get_list("todo_roles"))
    with ai_shell.change_directory("src"):
        await bot.initialize()
        bot.allow_self_certification = False
        await bot.basic_tool_loop(
            request, ".", tool_names, pytest_goal_checker, stop_on_no_tool_use=True  # root_folder,
        )
        print("Run completed.")


if __name__ == "__main__":
    asyncio.run(main())
