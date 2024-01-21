"""
Log a conversation to a file in Markdown format.
"""

import logging
import os
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Optional

import markpickle
import orjson as json

current_dir = os.path.dirname(os.path.abspath(__file__))
LOG_FOLDER = os.path.join(current_dir, "../dialog_log")


pickle_config = markpickle.Config(serialize_child_dict_as_table=False, serialize_dict_as_table=False)

logger = logging.getLogger(__name__)


def try_markpickle(value: Any) -> str:
    """
    Attempts to serialize the given value into a Markdown-formatted string using markpickle.

    Args:
        value (Any): The value to be serialized.

    Returns:
        str: A Markdown-formatted string representation of the value. If serialization fails,
             returns a plain string representation of the value.
    """
    try:
        return markpickle.dumps(value, config=pickle_config)
    except BaseException:
        return str(value)


class DialogLoggerWithMarkdown:
    """
    A class for logging dialog interactions in Markdown format.

    Attributes:
        bot_name (str): Name of the bot.
        model (str): Model used by the bot.
        bot_instructions (str): Instructions or description for the bot.
        base_directory (str): Base directory for storing log files.

    Methods:
        write_header: Writes the header information to the log file.
        add_user: Logs the user's input text.
        add_bot: Logs the bot's response text.
        add_toolkit: Logs the tools used in the dialog.
        add_tool: Logs a single tool and its arguments used in the dialog.
        add_tool_result: Logs the results from a tool.
        add_error: Logs an error that occurred during the dialog.
        ensure_log: Context manager to ensure the log file is closed properly.
    """

    def __init__(self, base_directory: str) -> None:
        """
        Initializes the DialogLoggerWithMarkdown object.

        Args:
            base_directory (str, optional): Base directory for storing log files. Defaults to LOG_FOLDER if not provided.
        """
        if not base_directory:
            raise ValueError("base_directory must be provided.")
        os.makedirs(base_directory, exist_ok=True)
        self.bot_name: Optional[str] = None
        self.model: Optional[str] = None
        self.bot_instructions: Optional[str] = None
        self.base_directory = base_directory
        log_files = [f for f in os.listdir(self.base_directory) if f.endswith(".md")]
        log_number = len(log_files) + 1
        self.log_file_path = os.path.join(self.base_directory, f"dialog_{log_number}.md")
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)

        # Context manager handles this, I think.
        # pylint: disable=consider-using-with
        self.log_file = open(self.log_file_path, "a", buffering=1, encoding="utf-8")
        self.pending_tools: dict[str, dict[str, str]] = {}

    def write_header(self, bot_name: str, model: str, bot_instructions: str) -> None:
        """
        Writes the header information to the log file.

        Args:
            bot_name (str): Name of the bot.
            model (str): Model used by the bot.
            bot_instructions (str): Instructions or description for the bot.
        """
        self.bot_name = bot_name
        self.model = model
        self.bot_instructions = bot_instructions
        header = f"# Bot Name: {self.bot_name}\n## Model: {self.model}\n### Instructions: {self.bot_instructions}\n\n"
        self.log_file.write(header)
        logger.info(header)

    def add_user(self, text: str) -> None:
        """
        Logs the user's input text.

        Args:
            text (str): The text input by the user.
        """
        users_message = f"**User**: {text}"
        self.log_file.write(f"{users_message}\n\n")
        logger.info(users_message)

    def add_bot(self, text: str) -> None:
        """
        Logs the bot's response text.

        Args:
            text (str): The text response from the bot.
        """
        bots_message = f"**Bot**: {text}"
        self.log_file.write(f"{bots_message}\n\n")
        logger.info(bots_message)

    def add_toolkit(self, tools: list[str]) -> None:
        """
        Logs the tools used in the dialog.

        Args:
            tools (List[str]): A list of tool names used in the dialog.
        """
        toolkit_str = "\n- ".join([f"`{tool}`" for tool in tools])
        toolkit_message = f"**Toolkit**: \n\n- {toolkit_str}"
        self.log_file.write(f"{toolkit_message}\n\n")
        logger.info(toolkit_message.replace("\n", ""))

    def add_tool(self, tool_call_id: str, tool_name: str, tool_args: str) -> None:
        """
        Logs a single tool and its arguments used in the dialog.

        Args:
            tool_call_id (str): The unique identifier for the tool call.
            tool_name (str): The name of the tool.
            tool_args (str): The arguments passed to the tool, in JSON string format.
        """
        bot_wants = f"Bot wants to use `{tool_name}`\n"
        self.log_file.write(bot_wants)
        logger.info(bot_wants)
        try:
            json_bits = json.loads(tool_args)
        except BaseException:
            self.log_file.write(f"Bot gave us Bad JSON: {tool_args}")
            self.pending_tools[tool_call_id] = {"tool_name": tool_name, "tool_args": tool_args}
            return
        args_lines: list[str] = []
        for name, value in json_bits.items():
            if value is not None:
                pair = f"{name} : {value}"
                args_lines.append(f" - {pair}\n")
                # logger.info(pair)
        self.pending_tools[tool_call_id] = {"tool_name": tool_name, "tool_args": "\n".join(args_lines)}

    def add_tool_result(self, tool_results: list[dict[str, Any]]) -> None:
        """
        Logs the results from a tool.

        Args:
            tool_results (List[Dict[str, Any]]): A list of dictionaries containing the tool results.
        """
        # result should always be of the same dict type
        # tool_result = {"tool_call_id": tool_call.id, "output": json_result}
        for result in tool_results:
            self.log_file.write("### Result\n\n")
            self.log_file.write(f"Tool call Id: {result['tool_call_id']}\n")
            self.log_file.write(f"Tool name: {self.pending_tools[result['tool_call_id']]['tool_name']}\n")
            self.log_file.write(f"Tool args:\n {self.pending_tools[result['tool_call_id']]['tool_args']}\n")
            del self.pending_tools["tool_call_id"]
            json_string = result["output"]
            # json.loads here should work, it isn't bot-json
            any_type = json.loads(json_string)
            if isinstance(any_type, dict):
                if "type" in any_type and "title" in any_type and "status" in any_type and "detail" in any_type:
                    self.log_file.write(f"ERROR: {any_type['type']} : {any_type['detail']}\n")
                else:
                    for key, value in any_type.items():
                        self.log_file.write(f" - {key} : {value}\n")
            else:
                self.log_file.write(f"{any_type}\n")

    def add_error(self, error: Exception) -> None:
        """
        Logs an error that occurred during the dialog.

        Args:
            error (Exception): The exception that was raised.
        """
        error_message = f"**Error**: {error}"
        self.log_file.write(f"{error_message}\n\n")
        logger.error(error_message)

    @contextmanager
    def ensure_log(self) -> Iterator[None]:
        """
        A context manager to ensure that the log file is closed properly.

        Yields:
            None: Yields control to the block of code using this context manager.

        Ensures:
            The log file is closed properly upon exiting the block of code.
        """
        try:
            yield
        finally:
            self.log_file.close()


if __name__ == "__main__":

    def run() -> None:
        bot_name = "Botty bot"
        model = "blah"
        bot_instructions = "Let's do the thing."
        # Example of using the updated class with Markdown formatting
        dialog_logger_md = DialogLoggerWithMarkdown("./tmp")
        dialog_logger_md.write_header(bot_name, model, bot_instructions)

        # Using the context manager to ensure proper logging
        with dialog_logger_md.ensure_log():
            dialog_logger_md.add_user("Hello, bot!")
            dialog_logger_md.add_bot("Hello, user!")
            dialog_logger_md.add_toolkit(["python", "dalle"])
            dialog_logger_md.add_tool("xyzzy", "python", "calculate something")
            # In case of an error
            # dialog_logger_md.add_error("Some error occurred")

    run()
