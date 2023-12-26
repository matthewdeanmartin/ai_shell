"""
Optimized for AI version of pytest.
"""
from ai_shell.externals.pytest_call import count_pytest_results
from ai_shell.utils.cwd_utils import change_directory
from ai_shell.utils.logging_utils import log


class PytestTool:
    """Optimized for AI version of pytest."""

    def __init__(self, root_folder: str) -> None:
        """
        Initialize the PytestTool class.

        Args:
            root_folder (str): The root folder path for file operations.
        """
        self.root_folder = root_folder

        # TODO: to provide via config.
        self.module = "fish_tank"
        self.tests_folder = "tests"
        self.min_coverage = 80

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
            passed_tests, failed_tests, coverage, command_result = count_pytest_results(
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
    print(PytestTool(root_folder="e:/github/ai_shell/src").pytest())
