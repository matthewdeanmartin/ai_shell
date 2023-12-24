import dataclasses
import os
from datetime import datetime

import openai
import toml


@dataclasses.dataclass
class Thread:
    id: str
    timestamp: str = dataclasses.field(default_factory=lambda: datetime.now().isoformat())


@dataclasses.dataclass
class Bot:
    assistant_id: str
    name: str
    threads: list[Thread] = dataclasses.field(default_factory=list)

    def add_thread(self, thread_id):
        self.threads.append(Thread(thread_id))


class Config:
    def __init__(self):
        self.config_file = os.getenv("CONFIG_PATH", "config.toml")
        self.data = {
            "bots": [],
            "flags": {
                "enable_tool_selector_bot": False,
                "enable_regex_tester_bot": False,
                "enable_prompt_improver_bot": False,
                "enable_dialog_log": False,
                "enable_shell_log": False,
                "enable_api_log": False,
                "enable_autocat": True,
            },
        }
        self.load_config()

    def load_config(self):
        if os.path.isfile(self.config_file):
            self.data = toml.load(self.config_file)
        else:
            self.save_config()
        if len(self.data.setdefault("bots", [])) > 5:
            raise ValueError("You have too many bots. Bot persistence must be failing somewhere.")

    def save_config(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            toml.dump(self.data, f)

    def add_bot(self, assistant_id: str, name: str):
        bot = Bot(assistant_id, name)
        self.data.setdefault("bots", []).append(dataclasses.asdict(bot))
        self.save_config()

    def set_flag(self, flag_name, value):
        if flag_name in self.data["flags"]:
            self.data["flags"][flag_name] = value
            self.save_config()

    def cleanup(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        existing_bots = openai.beta.assistants.list()
        assistant_ids = [bot.id for bot in existing_bots.data]

        # Remove bots that no longer exist in OpenAI
        self.data["bots"] = [bot for bot in self.data["bots"] if bot["assistant_id"] in assistant_ids]
        self.save_config()

    def get_bots(self):
        return [Bot(**bot) for bot in self.data["bots"]]

    def get_bot(self, name):
        for bot in self.data.setdefault("bots", []):
            if bot["name"] == name:
                return Bot(**bot)
        return None

    def get_flag(self, flag_name):
        return self.data["flags"].get(flag_name, None)


if __name__ == "__main__":

    def run():
        # Note: For the cleanup function to work, you need to have the OpenAI API key set and the openai library installed.

        # Example Usage
        config = Config()
        config.add_bot("assistant_123", "MyBot")
        config.set_flag("enable_tool_selector_bot", True)
        # Call config.cleanup() to remove bots that have been deleted on OpenAI's side.

    run()
