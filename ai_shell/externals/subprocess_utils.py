import dataclasses
import shlex  # nosec
import subprocess  # nosec


@dataclasses.dataclass
class CommandResult:
    stdout: str
    stderr: str
    return_code: int


def safe_subprocess(command_name: str, arg_string: str, markdown: bool = True):
    # Split the command using shlex
    args = shlex.split(f"{command_name} {arg_string}")
    # Execute the command
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)  # nosec
    stdout, stderr = process.communicate()
    # Get the return code
    return_code = process.returncode

    if markdown:
        error_text = f"### Standard Error\n{stderr.decode()}" if stderr else ""
        args_markdown = f"## Arguments\n{args}" if args else ""
        # Format the output as Markdown
        markdown_output = f"""## {command_name} Output
{args_markdown}
### Standard Output
{stdout.decode()}
{error_text}
### Return Code
`{return_code}`"""
        return markdown_output
    return CommandResult(stdout.decode(), stderr.decode(), return_code)
