"""
Call black to check if the python source is now hosed so bad it can't format it.
"""

from ai_shell.externals.subprocess_utils import CommandResult, safe_subprocess


def invoke_black(file_path: str) -> CommandResult:
    """
    Runs black on the file or folder. Code 128 means the file is hosed.

    Args:
        file_path (str): The name of the module to run black on.

    Returns:
        CommandResult: The result of the command.
    """
    command_name = "black"
    arg_string = f"'{file_path}' --check"

    return safe_subprocess(command_name, arg_string)


# if __name__ == "__main__":
#     # Example usage
#     markdown_document = invoke_pylint(f"pylint {__file__}")
#     print(markdown_document)
