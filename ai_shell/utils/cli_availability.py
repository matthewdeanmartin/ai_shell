"""
Check if an external tool is expected and available on the PATH.

Also, check version.
"""

import shutil
import subprocess  # nosec
from typing import Optional

import toml


def read_cli_tools_from_pyproject(file_path: str) -> dict[str, dict[str, str]]:
    """
    Read the cli-tools section from a pyproject.toml file.

    Args:
        file_path (str): The path to the pyproject.toml file.

    Returns:
        dict[str, dict[str, str]]: A dictionary with the cli-tools section.
    """
    try:
        with open(file_path) as file:
            pyproject_data = toml.load(file)
        return pyproject_data.get("tool", {}).get("cli-tools", {})
    except Exception as e:
        print(f"Error reading pyproject.toml: {e}")
        return {}


def check_tool_availability(tool_name: str, version_switch: Optional[str] = None):
    """
    Check if a tool is available in the system's PATH.

    Args:
        tool_name (str): The name of the tool to check.
        version_switch (Optional[str]): The switch to get the tool version. Defaults to None.

    Returns:
        Tuple[bool, Optional[str]]: A tuple with the first element being True if the tool is available, False otherwise.
            The second element is the tool version if version_switch is provided, None otherwise.
    """
    # Check if the tool is in the system's PATH
    if not shutil.which(tool_name):
        return False, None

    # If version_switch is provided, try to get the version
    version = None
    if version_switch:
        try:
            result = subprocess.run([tool_name, version_switch], capture_output=True, text=True, shell=False)  # nosec
            out = result.stdout.strip()
            if "\n" in out:
                version = out.split("\n")[0]
            else:
                version = result.stdout.strip()
        except Exception as exception:
            print(exception)

    return True, version


if __name__ == "__main__":

    def run() -> None:
        """Example"""
        # Example usage
        file_path = "../../pyproject.toml"  # Replace with the path to your pyproject.toml
        cli_tools = read_cli_tools_from_pyproject(file_path)

        for tool, config in cli_tools.items():
            is_available, version = check_tool_availability(tool, config.get("version_switch"))
            print(
                f"{tool}: {'Available' if is_available else 'Not Available'} - Version: {version if version else 'N/A'}"
            )

    run()
