"""
Safe, token-aware filesystem tools for LLM agents.

`ai_shell` provides familiar shell-like tools (cat, ls, grep, find, head/tail,
cut, sed, git, ...) reimplemented in pure Python, jailed to a root folder and
tuned to return useful, token-bounded output. They are provider-agnostic: wire
them into any agent via the generated JSON Schemas and the neutral dispatch
table (`ToolKit`).

.. include:: ../README.md
"""

from ai_shell.ai_logs.logging_utils import configure_logging
from ai_shell.answer_tool import AnswerCollectorTool
from ai_shell.cat_tool import CatTool
from ai_shell.cut_tool import CutTool
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
from ai_shell.patch_tool import PatchTool
from ai_shell.pycat_tool import PyCatTool
from ai_shell.pytest_tool import PytestTool
from ai_shell.replace_tool import ReplaceTool
from ai_shell.rewrite_tool import RewriteTool
from ai_shell.sed_tool import SedTool
from ai_shell.todo_tool import TodoTool
from ai_shell.token_tool import TokenCounterTool
from ai_shell.toolkit import ToolKit
from ai_shell.tools_registry import ALL_TOOLS, initialize_all_tools, initialize_recommended_tools
from ai_shell.utils.config_manager import Config
from ai_shell.utils.cwd_utils import change_directory

__all__ = [
    # tools
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
    "SedTool",
    "ReplaceTool",
    "InsertTool",
    "TodoTool",
    "AnswerCollectorTool",
    "PytestTool",
    # registry / dispatch
    "ToolKit",
    "ALL_TOOLS",
    "initialize_all_tools",
    "initialize_recommended_tools",
    "Config",
    # logging
    "configure_logging",
    # goal-checker helpers (optional)
    "invoke_pylint",
    "pytest_call",
    "invoke_black",
    "count_lines_of_code",
    # misc
    "change_directory",
]
