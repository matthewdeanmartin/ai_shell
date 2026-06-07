"""A module for managing the ai_shell.toml file."""

import os

import toml

from ai_shell.utils.json_utils import FatalConfigurationError


class Config:
    """A class for managing the ai_shell.toml file.

    This is for globally available settings that the model shouldn't (or can't) set,
    e.g. read-only mode, the plugin folder, and tool defaults.
    """

    def __init__(self, config_path: str = "") -> None:
        """Initialize the Config class."""
        if config_path and config_path.endswith(".toml"):
            self.config_file = config_path
        elif config_path:
            self.config_file = os.path.join(config_path, "ai_shell.toml")
        else:
            self.config_file = os.getenv("CONFIG_PATH", "ai_shell.toml")
        # freeze the location of the config file
        self.config_file = os.path.abspath(self.config_file)
        self._list_data: dict[str, list[str]] = {}
        self._values_data: dict[str, str] = {}
        self._flags_data: dict[str, bool] = {
            "enable_autocat": True,
        }
        self.load_config()

    def load_config(self) -> None:
        """Load the config from the config file."""
        if os.path.isfile(self.config_file):
            data = toml.load(self.config_file)
            self._flags_data = data.get("flags", self._flags_data)
            self._values_data = data.get("values", {})
            self._list_data = data.get("lists", {})
        else:
            self.save_config()

    def save_config(self) -> None:
        """Save the config to the config file."""
        if not os.path.isabs(self.config_file):
            raise ValueError("Config file path must be absolute.")
        with open(self.config_file, "w", encoding="utf-8") as f:
            toml.dump(
                {
                    "flags": self._flags_data,
                    "values": self._values_data,
                    "lists": self._list_data,
                },
                f,
            )

    def set_flag(self, flag_name: str, value: bool) -> None:
        """Set the value of the given flag.

        Args:
            flag_name (str): The name of the flag.
            value (bool): The value of the flag.
        """
        self._flags_data[flag_name] = value
        self.save_config()

    def get_flag(self, flag_name: str, default_value: bool | None = None) -> bool | None:
        """Return the value of the given flag.

        Args:
            flag_name (str): The name of the flag.
            default_value (Optional[bool]): The default to return if the flag is unset.

        Returns:
            Optional[bool]: The value of the flag, or the default.
        """
        return self._flags_data.get(flag_name, default_value)

    def get_value(self, name: str, default: str | None = None) -> str | None:
        """Return the value of the given named value.

        Args:
            name (str): The name of the config value.
            default (Optional[str]): The default to return if unset.

        Returns:
            Optional[str]: The value, or the default.
        """
        return self._values_data.get(name, default)

    def get_required_value(self, name: str) -> str:
        """Return a required named value.

        Args:
            name (str): The name of the config value.

        Returns:
            str: The value.

        Raises:
            FatalConfigurationError: If the value does not exist.
        """
        value = self._values_data.get(name, None)
        if value is None:
            raise FatalConfigurationError(f"Need {name} in config file")
        return value

    def set_list(self, list_name: str, value: list[str]) -> None:
        """Set a named list.

        Args:
            list_name (str): The name of the list.
            value (list[str]): The list contents.
        """
        self._list_data[list_name] = value
        self.save_config()

    def get_list(self, list_name: str) -> list[str]:
        """Return a named list.

        Args:
            list_name (str): The name of the list.

        Returns:
            list[str]: The list, or empty.
        """
        return self._list_data.get(list_name, [])
