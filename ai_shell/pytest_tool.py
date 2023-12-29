"""
Optimized for AI version of pytest.
"""
from ai_shell.externals.pytest_call import count_pytest_results
from ai_shell.utils.config_manager import Config
from ai_shell.utils.cwd_utils import change_directory
from ai_shell.utils.logging_utils import log


class PytestTool:
    """Optimized for AI version of pytest."""

    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the PytestTool class.

        Args:
            root_folder (str): The root folder path for file operations.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder

        self.config = config
        self.module = config.get_value("pytest_module")
        self.tests_folder = config.get_value("pytest_folder")

        self.min_coverage = float(config.get_value("pytest_min_coverage") or 0.0)

    @log()
    def pytest(
        self,
    ) -> str:
        """
        Runs pytest on tests in tests folder..

        Returns:
            str: Output from pytest.
        """
        with change_directory(self.root_folder):
            # What is -rA
            if not self.module:
                return "No module set for pytest, please set in ai_config.toml"
            if not self.tests_folder:
                return "No tests folder set for pytest, please set in ai_config.toml"
            if not self.min_coverage:
                return "No min coverage set for pytest, please set in ai_config.toml"
            _passed_tests, _failed_tests, _coverage, command_result = count_pytest_results(
                self.module, self.tests_folder, self.min_coverage
            )
            markdown_output = f"""## Pytest Output
### Standard Output
{command_result.stdout}
### Standard Error
{command_result.stderr}
### Return Code
`{command_result.return_code}`"""
            return markdown_output


if __name__ == "__main__":
    print(PytestTool(root_folder="../src", config=Config("..")).pytest())
