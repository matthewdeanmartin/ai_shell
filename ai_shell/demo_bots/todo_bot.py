"""
Bot that looks for TODOs and tracks them.
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

    short_name = "todo"
    source = files("ai_shell").joinpath(f"demo_bots/{short_name}_bot_instructions.md")
    with open(str(source), encoding="utf-8") as instructions:
        bot_instructions = instructions.read()
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
        "grep_markdown",
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
        # "insert_text_after_context",
        # "insert_text_after_multiline_context",
        # "insert_text_at_start_or_end",
        #
        # "replace_all",
        # "replace_line_by_line",
        # "replace_with_regex",
        #
        # "apply_git_patch",
        # "rewrite_file",
        # "write_new_file",
        # "sed",
        # # python specific
        # "pytest",
        # # "save_if_changed",
        # TODO management
        "add_todo",
        "query_todos_by_assignee",
        "query_todos_by_regex",
        "remove_todo",
        # # Utility
        # "count_tokens",
    ]
    bot_name = "Python Business Analyst Bot."

    root_folder = "src"
    if not os.path.exists(root_folder):
        raise ValueError("The demo requires that there be a src folder with some python code in it.")
    dialog_logger_md = ai_shell.DialogLoggerWithMarkdown("./tmp")

    source = files("ai_shell").joinpath(f"demo_bots/{short_name}_bot_mission.md")
    with open(str(source), encoding="utf-8") as instructions:
        request = instructions.read()

    goal_todos = 10

    async def static_keep_going(toolkit: ai_shell.ToolKit) -> str:
        """Check goal"""
        used: list[str] = []
        total_usages = 0
        for tool in tool_names:
            usage = toolkit.get_tool_usage_for(tool)
            used.append(tool)
            total_usages += usage["count"]

        print("TODOs so far:")
        print(tm.query_by_title_keyword(""))

        if total_usages == 0:
            # Nothing done!
            return (
                "You haven't used any tools yet, how can you learn about the project without browsing the files?"
                "Please keep going, view the files and find the thins that need to be done. "
                f"Add TODOs with add_todo: {', '.join(tool_names)}."
            )

        stats = tm.get_stats_numeric()
        stats["Completed tasks"]
        stats["Incomplete tasks"]
        total = stats["Total tasks"]

        initial_stats["Completed tasks"]
        initial_stats["Incomplete tasks"]
        initial_total = initial_stats["Total tasks"]

        if total_usages > 0 and total == initial_total:
            # Tool usage, but no TODOs added.
            return (
                f"Thanks for doing preliminary research with the tools, don't forget the goal is to create TODOs. "
                f"We still want at least {goal_todos} new TODOs"
            )

        if total > initial_total and total - initial_total < goal_todos:
            # Something done, but not all of them.
            return (
                f"This is looking good, we've added {total - initial_total} TODOs so far. "
                f"We still want at least {goal_todos-(total - initial_total)} more TODOs"
            )
        if total - initial_total >= goal_todos:
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
    tm = ai_todo.TaskManager("src", config.get_list("todo_roles"))
    initial_stats = tm.get_stats_numeric()
    with ai_shell.change_directory("src"):
        await bot.initialize()
        usage_count = await bot.basic_tool_loop(
            request, root_folder, tool_names, static_keep_going, stop_on_no_tool_use=False
        )
        logger.info(f"Run completed. tool usage count: {usage_count}")


if __name__ == "__main__":
    asyncio.run(main())
