"""
Filesystem shell tools for OpenAI Assistant
"""
from ai_shell.answer_tool import AnswerCollectorTool
from ai_shell.bot_glue.bot import TaskBot
from ai_shell.cat_tool import CatTool
from ai_shell.cut_tool import CutTool
from ai_shell.ed_tool import EdTool
from ai_shell.edlin_tool import EdlinTool
from ai_shell.externals import pytest_call
from ai_shell.externals.black_call import invoke_black
from ai_shell.externals.pygount_call import count_lines_of_code
from ai_shell.externals.pylint_call import invoke_pylint
from ai_shell.find_tool import FindTool
from ai_shell.git_tool import GitTool
from ai_shell.grep_tool import GrepTool
from ai_shell.head_tail_tool import HeadTailTool
from ai_shell.insert_tool import InsertTool
from ai_shell.ls_tool import LsTool
from ai_shell.openai_toolkit import ToolKit
from ai_shell.openai_tools import ALL_TOOLS, initialize_all_tools, initialize_recommended_tools
from ai_shell.patch_tool import PatchTool
from ai_shell.pycat_tool import PyCatTool
from ai_shell.pytest_tool import PytestTool
from ai_shell.replace_tool import ReplaceTool
from ai_shell.rewrite_tool import RewriteTool
from ai_shell.sed_tool import SedTool
from ai_shell.todo_tool import TodoTool
from ai_shell.token_tool import TokenCounterTool
from ai_shell.utils.config_manager import Config
from ai_shell.utils.cwd_utils import change_directory
from ai_shell.utils.log_conversation import DialogLoggerWithMarkdown
from ai_shell.utils.logging_utils import configure_logging

__all__ = [
    "CatTool",
    "CutTool",
    "FindTool",
    "GrepTool",
    "HeadTailTool",
    "LsTool",
    "GitTool",
    "TokenCounterTool",
    "PatchTool",
    "RewriteTool",
    "PyCatTool",
    "EdTool",
    "EdlinTool",
    "ToolKit",
    "SedTool",
    "ReplaceTool",
    "InsertTool",
    "TodoTool",
    "AnswerCollectorTool",
    "PytestTool",
    # Tool and general config
    "initialize_all_tools",
    "initialize_recommended_tools",
    "Config",
    "ALL_TOOLS",
    # logging support
    "configure_logging",
    "DialogLoggerWithMarkdown",
    # bot support
    "TaskBot",
    # goal checker tools
    "invoke_pylint",
    "pytest_call",
    "invoke_black",
    "count_lines_of_code",
    # misc that could have been 3rd party
    "change_directory",
]
