import os

from ai_shell import Config


def config_for_tests() -> Config:
    return Config(find_config_file())


def find_config_file():
    # Start with the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the name of your config file
    config_file_name = "ai_shell.toml"

    # Check in the current directory and parent directories
    for _ in range(5):  # Adjust the range as needed
        config_path = os.path.join(current_dir, config_file_name)
        if os.path.exists(config_path):
            return config_path
        # Go up one directory
        current_dir = os.path.dirname(current_dir)

    raise FileNotFoundError("Config file not found")


if __name__ == "__main__":
    print(find_config_file())
