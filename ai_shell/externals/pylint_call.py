from ai_shell.externals.subprocess_utils import safe_subprocess


def invoke_pylint(module_name: str) -> str:
    command_name = "pytest"
    arg_string = f"'{module_name}'"

    # generic response.
    return safe_subprocess(command_name, arg_string)


# if __name__ == "__main__":
#     # Example usage
#     markdown_document = invoke_pylint(f"pylint {__file__}")
#     print(markdown_document)
