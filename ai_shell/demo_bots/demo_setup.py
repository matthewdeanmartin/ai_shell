"""
Initialization for demo bots.
"""
import os
import zipfile
from importlib.resources import as_file, files
from pathlib import Path

from ai_shell.utils.config_manager import Config


def create_fish_tank() -> None:
    """
    Create the fish_tank demo app.
    """
    # Locate the resource file
    source = files("ai_shell").joinpath("fish_tank.zip")

    # Create the target directory if it doesn't exist
    target_dir = Path.cwd() / "src"

    if target_dir.exists() and any(target_dir.iterdir()):
        # this shouldn't happen.
        raise ValueError("The src folder already exists and has something in it.")

    # Unzip the file to the target directory
    with as_file(source) as file:
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall(Path.cwd())


def initialize() -> None:
    """
    Check if src folder exists.
    If not, ask user if they want to create the fish_tank demo app.
    If yes, create the fish_tank demo app.
    Once src exists, ask if they grant permission to modify it.
    Create config file in current directory.
    Check for openai key and .env file. If not found, explain how to get it and put into .env file.
    """
    if not os.path.exists("src"):
        print("The demo requires that there be a src folder with some python code in it.")
        print("Would you like to create the fish_tank demo app? (y/n)")
        response = input()
        if response.lower().startswith("y"):
            create_fish_tank()
        else:
            print("Ok, bye.")
            return
    else:
        print("The src folder exists. You are good to go.")

    print("Would you like to grant permission for the demo to modify the src folder? (y/n)")
    response = input()
    if response.lower().startswith("y"):
        print("Ok, we're good to go.")
    else:
        print("Ok, bye.")
        return

    if not os.path.exists("ai_shell.toml"):
        print("Creating config.")
        _ = Config()
    else:
        print("Config (ai_shell.toml) already exists.")

    if os.path.exists(".env"):
        print(".env file already exists.")
        with open(".env", encoding="utf-8") as f:
            env = f.read()
        if "OPENAI_KEY" in env:
            print("Found OPENAI_KEY in .env file.")
            print("We will assume for now it works.")
    else:
        print("Creating .env file.")
        with open(".env", "w", encoding="utf-8") as f:
            f.write("OPENAI_API_KEY=OPENAI_API_KEY\n")
        print("Created .env file. You will need to edit it with a valid OPENAI_KEY.")
        print("See more here: https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key")


if __name__ == "__main__":
    initialize()
