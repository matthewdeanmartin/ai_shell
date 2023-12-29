"""
Runs mypy.

External tools are not pure python and have subprocess risks.
"""
from ai_shell.externals.subprocess_utils import CommandResult, safe_subprocess


def invoke_mypy(module_name: str) -> CommandResult:
    """
    Runs mypy on the module.

    Args:
        module_name (str): The name of the module to run mypy on.

    Returns:
        CommandResult: The result of the command.
    """
    command_name = "mypy"
    arg_string = f"'{module_name}' --ignore-missing-imports"

    # generic response.
    return safe_subprocess(command_name, arg_string)


if __name__ == "__main__":
    # Example usage
    markdown_document = invoke_mypy("../../src/fish_tank")
    print(markdown_document.to_markdown())
