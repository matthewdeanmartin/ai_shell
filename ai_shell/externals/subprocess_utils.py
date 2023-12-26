"""
A module to provide a safe subprocess wrapper.
"""
import dataclasses
import shlex  # nosec
import subprocess  # nosec


@dataclasses.dataclass
class CommandResult:
    """A dataclass to hold the results of a subprocess command."""

    command_name: str
    args: list[str]
    stdout: str
    stderr: str
    return_code: int

    def to_markdown(self) -> str:
        error_text = f"### Standard Error\n{self.stderr}" if self.stderr else ""
        args_markdown = f"## Arguments\n{self.args}" if self.args else ""
        # Format the output as Markdown
        markdown_output = f"""## {self.command_name} Output
{args_markdown}
### Standard Output
{self.stdout}
{error_text}
### Return Code
`{self.return_code}`"""
        return markdown_output


def safe_subprocess(command_name: str, arg_string: str) -> CommandResult:
    """
    A wrapper around subprocess to safely execute a command.
    Args:
        command_name: The name of the command to execute.
        arg_string: The arguments to pass to the command.
        markdown: Whether to format the output as Markdown.

    Returns:
        The output of the command.
    """
    # Split the command using shlex
    args = shlex.split(f"{command_name} {arg_string}")
    # Execute the command
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)  # nosec
    stdout, stderr = process.communicate()
    # Get the return code
    return_code = process.returncode
    return CommandResult(command_name, args, stdout.decode(), stderr.decode(), return_code)
