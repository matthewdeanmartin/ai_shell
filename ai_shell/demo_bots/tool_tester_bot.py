"""
An example bot that will check if a tool works as expected.

The goal checker will check if the user has used tools that need testing.

(To be clear, this isn't the unit testing bot, that's example_test_writer_bot.py)
"""

import asyncio
import logging
import logging.config
import os
from importlib.resources import files

from dotenv import load_dotenv

import ai_shell
import ai_shell.demo_bots.demo_setup as demo_setup
import ai_todo

ai_shell.ai_logs.log_to_bash.LOGGING_ENABLED = True

if __name__ == "__main__" and not os.path.exists("src"):
    demo_setup.initialize()


async def main():
    load_dotenv()

    logger = logging.getLogger(__name__)
    logging.config.dictConfig(ai_shell.configure_logging())

    model = "gpt-3.5-turbo-1106"
    short_name = "tool_tester"
    source = files("ai_shell").joinpath(f"demo_bots/{short_name}_bot_instructions.md")
    with open(str(source), encoding="utf-8") as instructions:
        bot_instructions = instructions.read()
    #    bot_instructions = "You are a tool tester. You will test out tools and then provide a report on if they work the way you expected them to."
    tool_names = [
        # readonly
        # "cat",
        "cat_markdown",
        # "cut_characters",
        # "cut_fields",
        # "cut_fields_by_name",
        # "find_files",
        "find_files_markdown",
        # "grep",
        # "grep_markdown",
        # "head",
        "head_markdown",
        # "head_tail",
        # "tail",
        "tail_markdown",
        # "ls",
        "ls_markdown",
        # "format_code_as_markdown",
        #
        # # read only git
        # "get_current_branch",
        # "get_recent_commits",
        # "git_diff",
        # "git_diff_commit",
        # "git_log_file",
        # "git_log_search",
        # "git_show",
        # "git_status",
        # # "is_ignored_by_gitignore",
        #
        # # read write
        # "ed",
        # "edlin",
        #
        "insert_text_after_context",
        "insert_text_after_multiline_context",
        "insert_text_at_start_or_end",
        "replace_all",
        "replace_line_by_line",
        "replace_with_regex",
        #
        # "apply_git_patch",
        # "rewrite_file",
        "write_new_file",
        # "sed",
        # # python specific
        # "pytest",
        # # "save_if_changed",
        # TODO management
        "add_todo",
        # "query_todos_by_assignee",
        # "query_todos_by_regex",
        # "remove_todo",
        # # Utility
        # "count_tokens",
    ]
    bot_name = "Lead Software Validation Engineer."

    root_folder = "src"
    if not os.path.exists(root_folder):
        raise ValueError("The demo requires that there be a src folder with some python code in it.")
    dialog_logger_md = ai_shell.DialogLoggerWithMarkdown("./tmp")
    source = files("ai_shell").joinpath(f"demo_bots/{short_name}_bot_mission.md")
    with open(str(source), encoding="utf-8") as instructions:
        request = instructions.read()

    async def static_keep_going(toolkit: ai_shell.ToolKit) -> str:
        """Check goal"""
        not_used: list[str] = []
        used: list[str] = []
        total_usages = 0
        for tool in tool_names:
            usage = toolkit.get_tool_usage_for(tool)
            if usage["count"] == 0:
                not_used.append(tool)
            else:
                used.append(tool)
            total_usages += usage["count"]
        if not_used and total_usages == 0:
            # Nothing done!
            return f"You haven't used any tools yet, please keep going. We want to test: {', '.join(tool_names)}."

        if not_used and used and total_usages:
            # Something done, but not all of them.
            return (
                f"This is looking good, we've done {total_usages} tests with the tools so far. "
                f"We still need to test {', '.join(not_used)}"
            )
        if not_used:
            # This might not get called. Fallback for safety.
            return f"We still need to test {', '.join(not_used)}"
        if not not_used:
            return toolkit.conversation_over_marker
        raise TypeError("Why did we get here...")

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
    bot.allow_self_certification = False
    if not config.get_list("todo_roles"):
        config.set_list("todo_roles", ["Developer", "Tester"])
    ai_todo.TaskManager("src", config.get_list("todo_roles"))
    with ai_shell.change_directory("src"):
        await bot.initialize()
        usage_count = await bot.basic_tool_loop(
            request, ".", tool_names, static_keep_going, stop_on_no_tool_use=False  # root_folder,
        )
        logger.info(f"Run completed. tool usage count: {usage_count}")


if __name__ == "__main__":
    asyncio.run(main())
