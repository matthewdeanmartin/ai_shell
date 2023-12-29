"""
All the tools are optimized for LLMs, but not openai specifically.

This Toolkit and schemas handles some of the boilerplate for interfacing with
the openai python client.
"""
import json
import logging
import os
import traceback
from collections.abc import Callable
from typing import Any

from openai.types.beta.threads import Run

from ai_shell.import_plugins import convert_to_toolkit, handle_tool
from ai_shell.utils import medias
from ai_shell.utils.config_manager import Config
from ai_shell.utils.json_utils import LoosyGoosyEncoder, exception_to_rfc7807_dict, try_everything

logger = logging.getLogger(__name__)


class ToolKitBase:
    """Non generated base class for generated toolkit"""

    def __init__(
        self, root_folder: str, token_model: str, global_max_lines: int, permitted_tools: list[str], config: Config
    ) -> None:
        """
        Initialize the ToolKitBase class.

        Args:
            root_folder (str): The root folder path for file operations.
            token_model (str): The token model to use for the toolkit
            global_max_lines (int): The global max lines to use for the toolkit
            permitted_tools (list[str]): The permitted tools for the toolkit
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = os.path.abspath(root_folder)
        self.token_model = token_model
        self.global_max_lines = global_max_lines
        self._lookup: dict[str, Callable[[Any], Any]] = {}
        self.config = config
        self.plugin_folder = config.get_value("plugin_folder")
        self.plugin_tools: dict[str, Any] = (
            convert_to_toolkit(self.plugin_folder, root_folder) if self.plugin_folder else {}
        )

        self.permitted_tools: list[str] = permitted_tools
        self.tool_usage_stats: dict[str, dict[str, int]] = {}
        """Name: {count, success, failure}"""

    def get_tool_usage_for(self, name: str) -> dict[str, int]:
        """Get tool usage stats for a given tool

        Args:
            name (str): The tool name

        Returns:
            dict[str, int]: The tool usage stats
        """
        return self.tool_usage_stats.get(name, {"count": 0, "success": 0, "failure": 0})

    async def process_tool_calls(self, run: Run, write_json_to_logs=(lambda x, y: None)) -> list[Any]:
        """
        Process the tool calls in the run and return the results.

        Args:
            run (Run): The run to process
            write_json_to_logs (Callable[[Any, str], None]): A function that writes json to the logs

        Returns:
            list[Any]: The results of the tool calls
        """
        if not self._lookup:
            raise TypeError("Missing lookup table")
        results: list[dict[str, Any]] = []

        if not run.required_action:
            # This probably won't actually happen?
            return results
        for tool_call in run.required_action.submit_tool_outputs.tool_calls:
            logger.info(f"tool_call: {tool_call.function.name}")
            logger.info(f"tool_call: {tool_call.function.arguments}")
            name = tool_call.function.name

            self.tool_usage_stats[name] = self.tool_usage_stats.get(name, {"count": 0, "success": 0, "failure": 0})

            args_text = tool_call.function.arguments
            arguments = try_everything(args_text)
            if name not in self.permitted_tools:
                self.tool_usage_stats[name]["failure"] += 1
                raise PermissionError(
                    f"You haven't been granted the right to call the tool '{name}'. You can call "
                    f" these tools: {','.join(self.permitted_tools)}. If you still need {name}, "
                    f"please explain how it works and why you need it and the administrator will "
                    f"consider granting permissions."
                )
            if name in self._lookup:
                self.tool_usage_stats[name]["count"] += 1
                # TODO: assert pwd is self.root_folder already.
                # with temporary_change_dir(self.root_folder):
                try:
                    if "media_type" in arguments:
                        media_type = arguments["media_type"]
                        del arguments["media_type"]
                    else:
                        media_type = None
                    result = self._lookup[name](arguments)
                    self.tool_usage_stats[name]["success"] += 1
                    if media_type:
                        result = medias.convert_to_media_type(result, media_type)

                except Exception as exception:
                    self.tool_usage_stats[name]["failure"] += 1
                    print(exception)
                    traceback.print_exc()
                    result = exception_to_rfc7807_dict(exception)
                    logger.warning(f"Error in {name}: {result}")
            elif name in self.plugin_tools:
                # Refactor so plugin_tools are handled more like regular tools?
                # TODO: change folder, mimetypes, error handling, call stats, etc.
                tool_info = self.plugin_tools[name]
                method_name = name
                instance = tool_info[0]
                tool_info[1]
                bots_kwargs = arguments
                result = handle_tool(method_name, bots_kwargs, instance)
            else:
                self.tool_usage_stats[name]["failure"] += 1
                raise TypeError(f"Unknown function name {name}")
            tool_result = {
                "tool_call_id": tool_call.id,
                "output": json.dumps(result, cls=LoosyGoosyEncoder),
            }
            write_json_to_logs(tool_call, f"tool_call_{name}")
            write_json_to_logs(result, f"tool_result_{name}")

            results.append(tool_result)

        # Let library user submit_tool_outputs and poll the run
        logger.info(f"results: {results}")
        return results
