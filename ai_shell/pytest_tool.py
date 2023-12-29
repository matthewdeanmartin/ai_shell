"""
Optimized for AI version of pytest.
"""
from ai_shell.externals.pytest_call import count_pytest_results
from ai_shell.utils.config_manager import Config
from ai_shell.utils.json_utils import FatalConfigurationError
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
        # Host script must set env vars, temp folder location and pwd!
        # with change_directory(self.root_folder):
        # What is -rA
        if not self.module or not self.tests_folder or self.min_coverage:
            raise FatalConfigurationError("Please set in ai_config module, test_folder and min_coverage")
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
