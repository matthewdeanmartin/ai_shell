"""
Provider-agnostic tool dispatch.

The tools are optimized for LLMs but not for any specific vendor. This base class
handles the boilerplate of turning a tool name + argument dict (as produced by any
tool-calling model) into a result: permission gating, usage stats, media-type
handling, and error-to-RFC7807 conversion.
"""

import logging
import traceback
from collections.abc import Callable
from typing import Any

import orjson as json

from ai_shell.import_plugins import convert_to_toolkit, handle_tool
from ai_shell.utils import medias
from ai_shell.utils.config_manager import Config
from ai_shell.utils.json_utils import (
    FatalConfigurationError,
    exception_to_rfc7807_dict,
    loosy_goosy_default_encoder,
)

logger = logging.getLogger(__name__)


class FatalToolException(Exception):
    """A fatal tool error the model cannot recover from."""


class ToolKitBase:
    """Non-generated base class for the generated toolkit.

    Subclasses populate ``self._lookup`` with ``name -> callable(arguments)``.
    """

    def __init__(
        self, root_folder: str, token_model: str, global_max_lines: int, permitted_tools: list[str], config: Config
    ) -> None:
        """
        Args:
            root_folder (str): The root folder path for file operations.
            token_model (str): The token model to use for the toolkit.
            global_max_lines (int): The global max lines to use for the toolkit.
            permitted_tools (list[str]): The tools the caller is allowed to invoke.
            config (Config): Developer config the model shouldn't set.
        """
        import os

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
        """Get tool usage stats for a given tool.

        Args:
            name (str): The tool name.

        Returns:
            dict[str, int]: The tool usage stats.
        """
        return self.tool_usage_stats.get(name, {"count": 0, "success": 0, "failure": 0})

    def dispatch(self, name: str, arguments: dict[str, Any]) -> str:
        """Invoke a tool by name with a dict of arguments and return a JSON string.

        This is the neutral entry point: feed it the tool name and parsed arguments
        from any tool-calling model's response.

        Args:
            name (str): The tool name the model requested.
            arguments (dict[str, Any]): The parsed arguments.

        Returns:
            str: The tool result, JSON-encoded.
        """
        if not self._lookup:
            raise TypeError("Missing lookup table")

        self.tool_usage_stats.setdefault(name, {"count": 0, "success": 0, "failure": 0})

        if name not in self.permitted_tools:
            self.tool_usage_stats[name]["failure"] += 1
            raise PermissionError(
                f"You haven't been granted the right to call the tool '{name}'. You can call "
                f"these tools: {','.join(self.permitted_tools)}. If you still need {name}, "
                f"please explain how it works and why you need it and the administrator will "
                f"consider granting permissions."
            )

        if name in self._lookup:
            self.tool_usage_stats[name]["count"] += 1
            try:
                original_name = name
                media_type, name = self._media_type_to_method_name(arguments, name)

                result = self._lookup[name](arguments)
                self.tool_usage_stats[name]["success"] += 1

                if media_type and original_name == name:
                    result = medias.convert_to_media_type(result, media_type)

                if result is None:
                    raise FatalToolException("Never return None from a tool.")
                if result in ("", '""'):
                    logger.warning(f"Blank result from {name}. Why? {arguments}")
            except (FatalToolException, FatalConfigurationError):
                raise
            # pylint: disable=broad-exception-caught
            except Exception as exception:
                logger.error(exception)
                traceback.print_exc()
                self.tool_usage_stats[name]["failure"] += 1
                result = exception_to_rfc7807_dict(exception)
        elif name in self.plugin_tools:
            tool_info = self.plugin_tools[name]
            instance = tool_info[0]  # (instance, schema)
            result = handle_tool(name, arguments, instance)
        else:
            self.tool_usage_stats[name]["failure"] += 1
            raise TypeError(f"Unknown function name {name}")

        if isinstance(result, bytes):
            result = result.decode("utf-8")

        try:
            return json.dumps(result, default=loosy_goosy_default_encoder).decode("utf-8")
        except TypeError as type_error:
            logger.error(f"Error encoding result for {name}: {type_error}")
            logger.error(f"Result that json can't handle: {result}")
            raise

    def _media_type_to_method_name(self, arguments: dict[str, Any], name: str) -> tuple[str, str]:
        """Pop a ``mime_type`` argument and redirect to a markdown variant if asked.

        Args:
            arguments (dict[str, Any]): The arguments (mutated to remove mime_type).
            name (str): The tool name.

        Returns:
            tuple[str, str]: The media type (or None) and the resolved method name.
        """
        media_type = arguments.pop("mime_type", None)
        if media_type == "markdown":
            name = name + "_markdown"
        return media_type, name
