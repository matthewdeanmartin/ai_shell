"""
Runs pylint.

External tools are not pure python and have subprocess risks.
"""
from ai_shell.externals.subprocess_utils import CommandResult, safe_subprocess


def invoke_pylint(module_name: str, minimum_score: float) -> CommandResult:
    """
    Runs pylint on the module.

    Args:
        module_name (str): The name of the module to run pylint on.
        minimum_score (float): The minimum score to pass.

    Returns:
        CommandResult: The result of the command.
    """
    command_name = "pylint"
    arg_string = f"'{module_name}' --fail-under {minimum_score}"

    # generic response.
    return safe_subprocess(command_name, arg_string)


# if __name__ == "__main__":
#     # Example usage
#     markdown_document = invoke_pylint(f"pylint {__file__}")
#     print(markdown_document)
