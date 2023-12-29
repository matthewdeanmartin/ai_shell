"""
Call ruff to check if the python source is now hosed so bad it can't format it.
"""

from ai_shell.externals.subprocess_utils import CommandResult, safe_subprocess


def invoke_ruff(file_path: str) -> CommandResult:
    """
    Runs ruff on the file or folder.

    Args:
        file_path (str): The name of the module to run ruff on.

    Returns:
        CommandResult: The result of the command.
    """
    command_name = "ruff"
    arg_string = f"'{file_path}'"

    return safe_subprocess(command_name, arg_string)


if __name__ == "__main__":
    # Example usage
    markdown_document = invoke_ruff("../../src/fish_tank")
    print(markdown_document.to_markdown())
