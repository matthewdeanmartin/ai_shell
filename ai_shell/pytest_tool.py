"""
Optimized for AI version of pytest.
"""
from ai_shell.externals.subprocess_utils import safe_subprocess
from ai_shell.utils.cwd_utils import change_directory
from ai_shell.utils.logging_utils import log


class PytestTool:
    def __init__(self, root_folder: str) -> None:
        """
        Initialize the PytestTool class.

        Args:
            root_folder (str): The root folder path for file operations.
        """
        self.root_folder = root_folder
        self.tests_folder = "tests"

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
            return safe_subprocess("pytest", f"'{self.tests_folder}' -rA", markdown=True)


if __name__ == "__main__":
    print(PytestTool(root_folder="e:/github/ai_shell/src").pytest())
