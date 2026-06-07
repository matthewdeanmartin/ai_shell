import cli_tool_audit as audit
import cli_tool_audit.models as models


def validate_environment():
    """Check if external tools are available."""
    tool_configs = {}
    for tool, installer in (
        ("pytest", "pip"),
        ("pylint", "pipx"),
        ("black", "pipx"),
        ("pygount", "pipx"),
        ("ruff", "pip"),
    ):
        if installer == "pip":
            instructions = f"{tool} needs to be installed in the same virtual environment"
        else:
            instructions = f"{tool} can be pip installed, but I recommend globally installing with pipx"
        config = models.CliToolConfig(
            name=tool,
            version="*",
            version_switch="--version",
            schema=models.SchemaType.SEMVER,
            if_os=None,
            tags=None,
            install_command=f"{installer} install {tool}",
            install_docs=instructions,
        )
        tool_configs[tool] = config
    results = audit.process_tools(cli_tools=tool_configs, no_cache=True, tags=None, disable_progress_bar=True)
    for result in results:
        if result.is_problem():
            print(f"There is a problem with {result.tool}")
            if not result.is_available:
                print("It is not installed or not on the PATH.")
                print(f"Consider running `{result.tool_config.install_command}`")
            elif result.is_broken:
                print("It is installed and on the PATH, but I can't check its version.")
                print("It might be okay or it might not be.")
            elif not result.is_compatible:
                print("It is installed and on the PATH and runs, but appears to be the wrong version.")
                print(f"Compatibility report: {result.is_compatible}")
            print()
        else:
            print(f"{result.tool} is ready for the bot to use.")


if __name__ == "__main__":
    validate_environment()
