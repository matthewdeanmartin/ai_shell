"""
All the toolkit_factory are optimized for LLMs, but not openai specifically.

This Toolkit and schemas handles some of the boilerplate for interfacing with
the openai python client.
"""

import logging
from typing import Optional

from ai_shell.ls_tool import LsTool
from ai_shell.openai_schemas import SCHEMAS

logger = logging.getLogger(__name__)

ALL_TOOLS = []


def just_tool_names() -> list[str]:
    """Return a list of tool names"""
    names = []
    for _ns, tools in SCHEMAS.items():
        for name, _schema in tools.items():
            names.append(name)
    return names


def initialize_all_tools(skips: Optional[list[str]] = None, keeps: Optional[list[str]] = None) -> None:
    """Initialize all toolkit_factory"""
    if keeps is not None:
        keep = keeps
    elif skips is None:
        keep = just_tool_names()
    else:
        keep = [name for name in just_tool_names() if name not in skips]

    for _ns, tools in SCHEMAS.items():
        for name, schema in tools.items():
            function_style = {}
            function_style["name"] = name
            parameters = {"type": "object", "properties": schema["properties"], "required": schema["required"]}
            function_style["parameters"] = parameters
            function_style["description"] = schema["description"]
            if name in keep:
                ALL_TOOLS.append(function_style)
    logger.info(f"Active toolkit_factory {ALL_TOOLS}")


def recommendations(root_folder: str):
    """Recommend toolkit_factory based on the root folder."""
    tool = LsTool(root_folder)
    files = tool.ls("**/*")
    tool_set = set()
    all_of_em = just_tool_names()
    # Only need for csv and the like
    all_of_em.remove("cut")
    # Only need for python
    all_of_em.remove("pycat")

    for _file, file_type in files:
        if file_type == ".csv":
            tool_set.add("cut")
        elif file_type == ".py":
            tool_set.add("pycat")


def initialize_recommended_tools(root_folder: str) -> None:
    """Initialize recommended toolkit_factory"""
    initialize_all_tools(keeps=recommendations(root_folder))
