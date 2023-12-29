"""
This module contains a custom logging handler that writes JSON-formatted log messages to a folder.
"""
import ast
import json
from logging import Handler
from pathlib import Path


def almost_json_to_json(data_str: str) -> str:
    """
    Convert a string that is almost JSON into a JSON string.
    Args:
        data_str (str): A string that is almost JSON.

    Returns:
        str: A JSON string.
    """
    # Remove the initial "Request options:" part
    cleaned_data_str = data_str.replace("Request options:", "").replace("'HTTP Request:", "").strip()

    try:
        # Use ast.literal_eval to safely evaluate the string into a dictionary
        data_dict = ast.literal_eval(cleaned_data_str)

        # Convert the dictionary into a JSON string with indentation
        json_str = json.dumps(data_dict, indent=4)
    except BaseException:
        return data_str

    return json_str


class JSONFileHandler(Handler):
    """Logs openai requests to JSON files in a folder"""

    def __init__(self, directory: str, module_name: str) -> None:
        """
        Initialize the JSONFileHandler class.
        Args:
            directory (str): The directory path for file operations.
            module_name (str): The name of the module whose logs to write.
        """
        super().__init__()
        self.directory = directory
        self.module_name = module_name
        self.session_count = self._get_next_session_number()
        self.request_count = 1
        self._ensure_directory_exists()

    def emit(self, record):
        """Handles emitted records."""
        # Check if the message is from the specified module
        if record.name.startswith(self.module_name):
            try:
                # Process the log record
                message = self.format(record)  # bad idea?
                pretty_message = almost_json_to_json(message)

                # Write to a file
                filename = f"request_{self.request_count:03}.json"
                filepath = Path(self.directory, f"session{self.session_count}", filename)
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(pretty_message)
                self.request_count += 1
            except Exception:
                self.handleError(record)

    def _ensure_directory_exists(self):
        """Creates the directory if it doesn't exist."""
        Path(self.directory, f"session{self.session_count}").mkdir(parents=True, exist_ok=True)

    def _get_next_session_number(self):
        """Returns the next session number."""
        session_dir = Path(self.directory)
        if not session_dir.exists():
            return 1
        return len([d for d in session_dir.iterdir() if d.is_dir()]) + 1
