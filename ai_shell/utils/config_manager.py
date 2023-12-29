"""A module for managing the ai_shell.toml file."""
# pylint: disable=wrong-import-position, using-constant-test
import dataclasses
import os
from datetime import datetime
from typing import Optional

if True:
    import openai_multi_tool_use_parallel_patch

    if not openai_multi_tool_use_parallel_patch:
        print("Needs to not move!")
import openai
import toml


@dataclasses.dataclass
class Thread:
    """A class for managing threads."""

    id: str
    timestamp: str = dataclasses.field(default_factory=lambda: datetime.now().isoformat())


@dataclasses.dataclass
class Bot:
    """A class for managing bots."""

    assistant_id: str
    name: str
    threads: list[Thread] = dataclasses.field(default_factory=list)

    def add_thread(self, thread_id: str) -> None:
        """Add a thread to the bot.
        Args:
            thread_id (str): The ID of the thread.
        """
        self.threads.append(Thread(thread_id))


class Config:
    """A class for managing the ai_shell.toml file.

    This is for globally available things that shouldn't or can't be set by the bot.
    """

    def __init__(self, config_path: str = "") -> None:
        """Initialize the Config class."""
        if config_path and config_path.endswith(".toml"):
            self.config_file = config_path
        elif config_path:
            self.config_file = os.path.join(config_path, "ai_shell.toml")
        else:
            self.config_file = os.getenv("CONFIG_PATH", "ai_shell.toml")

        self._list_data: dict[str, list[str]] = {}
        self._values_data: dict[str, str] = {}
        self._flags_data: dict[str, bool] = {
            "enable_tool_selector_bot": False,
            "enable_regex_tester_bot": False,
            "enable_prompt_improver_bot": False,
            "enable_dialog_log": False,
            "enable_shell_log": False,
            "enable_api_log": False,
            "enable_autocat": True,
        }
        self._bots_data: list = []
        self.load_config()

    def load_config(self) -> None:
        """Load the config from the config file."""
        if os.path.isfile(self.config_file):
            data = toml.load(self.config_file)
            self._flags_data = data["flags"]
            self._bots_data = data["bots"]
            self._values_data = data["values"]
            self._list_data = data["lists"]
        else:
            self.save_config()
        if len(self._bots_data) > 5:
            raise ValueError("You have too many bots. Bot persistence must be failing somewhere.")

    def save_config(self):
        """Save the config to the config file."""
        with open(self.config_file, "w", encoding="utf-8") as f:
            toml.dump(
                {
                    "flags": self._flags_data,
                    "bots": self._bots_data,
                    "values": self._values_data,
                    "lists": self._list_data,
                },
                f,
            )

    def add_bot(self, assistant_id: str, name: str) -> None:
        """Add a bot to the config.
        Args:
            assistant_id (str): The ID of the bot.
            name (str): The name of the bot.
        """
        bot = Bot(assistant_id, name)
        self._bots_data.append(dataclasses.asdict(bot))
        self.save_config()

    def set_flag(self, flag_name: str, value: bool) -> None:
        """Set the value of the given flag.
        Args:
            flag_name (str): The name of the flag.
            value (str): The value of the flag.
        """
        if flag_name in self._flags_data:
            self._flags_data[flag_name] = value
            self.save_config()

    def cleanup(self) -> None:
        """Remove bots that have been deleted on OpenAI's side."""
        openai.api_key = os.getenv("OPENAI_API_KEY")
        existing_bots = openai.beta.assistants.list()
        assistant_ids = [bot.id for bot in existing_bots.data]

        # Remove bots that no longer exist in OpenAI
        self._bots_data = [bot for bot in self._bots_data if bot["assistant_id"] in assistant_ids]
        self.save_config()

    def get_bots(self) -> list[Bot]:
        """Return a list of Bot objects."""
        return [Bot(**bot) for bot in self._bots_data]

    def get_bot(self, name: str) -> Optional[Bot]:
        """Return a Bot object with the given name.
        Args:
            name (str): The name of the bot.

        Returns:
            Optional[Bot]: The bot with the given name, or None if no bot with that name exists.
        """
        for bot in self._bots_data:
            if bot["name"] == name:
                return Bot(**bot)
        return None

    def get_flag(self, flag_name: str) -> Optional[bool]:
        """Return the value of the given flag.
        Args:
            flag_name (str): The name of the flag.

        Returns:
            Optional[bool]: The value of the flag, or None if the flag does not exist.
        """
        return self._flags_data.get(flag_name, None)

    def get_value(self, name: str) -> Optional[str]:
        """Return the value of the given flag.
        Args:
            name (str): The name of the config value.

        Returns:
            Optional[str]: The value of the flag, or None if the flag does not exist.
        """
        return self._values_data.get(name, None)

    def get_list(self, list_name: str) -> list[str]:
        """Return the value of the given flag.
        Args:
            list_name (str): The name of the config value.

        Returns:
            list[str]: The list from the config file.
        """
        return self._list_data.get(list_name, [])


if __name__ == "__main__":

    def run():
        """Example Usage"""
        # Note: For the cleanup function to work, you need to have the OpenAI API key set and the openai library installed.

        config = Config()
        config.add_bot("assistant_123", "MyBot")
        config.set_flag("enable_tool_selector_bot", True)
        # Call config.cleanup() to remove bots that have been deleted on OpenAI's side.

    run()
