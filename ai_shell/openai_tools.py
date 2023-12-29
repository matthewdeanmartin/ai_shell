"""
All the tools are optimized for LLMs, but not openai specifically.

This Toolkit and schemas handles some of the boilerplate for interfacing with
the openai python client.
"""

import logging
from collections.abc import Collection
from typing import Any, Optional, Union

from ai_shell.ls_tool import LsTool
from ai_shell.openai_schemas import _SCHEMAS
from ai_shell.utils.config_manager import Config

logger = logging.getLogger(__name__)

ALL_TOOLS: list[dict[str, Any]] = []


def just_tool_names() -> list[str]:
    """Return a list of tool names

    Returns:
        list[str]: A list of tool names
    """
    names = []
    for _ns, tools in _SCHEMAS.items():
        for name, _schema in tools.items():
            names.append(name)
    return names


def initialize_all_tools(skips: Optional[list[str]] = None, keeps: Optional[list[str]] = None) -> None:
    """Initialize all tools

    Args:
        skips (Optional[list[str]], optional): Tools to skip. Defaults to None.
        keeps (Optional[list[str]], optional): Tools to keep. Defaults to None.
    """
    if keeps is not None:
        keep = keeps
    elif skips is None:
        keep = just_tool_names()
    else:
        keep = [name for name in just_tool_names() if name not in skips]

    for _ns, tools in _SCHEMAS.items():
        for name, schema in tools.items():
            function_style: dict[str, Union[str, Collection[str]]] = {"name": name}
            parameters = {"type": "object", "properties": schema["properties"], "required": schema["required"]}
            function_style["parameters"] = parameters
            function_style["description"] = schema["description"]
            if name in keep:
                ALL_TOOLS.append(function_style)
    active_tools_string = ", ".join(tool["name"] for tool in ALL_TOOLS)
    logger.info(f"Active tools {active_tools_string}")


def recommendations(root_folder: str, config: Config) -> list[str]:
    """Recommend tools based on the root folder.

    Args:
        root_folder (str): The root folder to recommend tools for.
        config (Config): The developer input that bot shouldn't set.

    Returns:
        list[str]: A list of recommended tools.
    """
    tool = LsTool(root_folder, config)
    files = tool.ls("**/*")
    tool_set = set()
    all_of_em = just_tool_names()

    # Only need for csv and the like
    all_of_em.remove("cut")

    # Only need for python
    all_of_em.remove("pycat")
    all_of_em.remove("pytest")
    # Other python themed tools.

    # TODO: detect git repo & if not git, remove git.
    # all_of_em.remove("git")

    for _file, file_type in files:
        if file_type == ".csv":
            tool_set.add("cut")
        elif file_type == ".py":
            tool_set.add("pycat")
    return list(tool_set)


def initialize_recommended_tools(root_folder: str, config: Config) -> None:
    """Initialize recommended tools

    Args:
        root_folder (str): The root folder to recommend tools for.
        config (Config): The developer input that bot shouldn't set.
    """
    initialize_all_tools(keeps=recommendations(root_folder, config))
