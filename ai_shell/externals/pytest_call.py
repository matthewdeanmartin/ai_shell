"""
Runs pytest.

External tools are not pure python and have subprocess risks.
"""
import re

from ai_shell.externals.subprocess_utils import CommandResult, safe_subprocess
from ai_shell.utils.cwd_utils import change_directory

# TODO: lint the tests
# def lint_unittests():
#     """ "
#     pylint-unittest 0.2.0
#     pylint --load-plugins pylint_unittest"""


def count_pytest_results(module: str, test_folder: str, min_coverage: float) -> tuple[int, int, float, CommandResult]:
    """
    Run pytest and count the number of passed and failed tests.

    Args:
        module (str): The module to run pytest on.
        test_folder (str): The folder containing the tests.
        min_coverage (float): The minimum coverage percentage.

    Returns:
        A tuple of the number of passed and failed tests.
    """
    args = f"{test_folder} --cov={module} --cov-report term --cov-fail-under {min_coverage}"
    # Run pytest using safe_subprocess
    pytest_output = safe_subprocess("pytest", args)

    # Low coverage shows as error.
    # # Check if there was an error running pytest
    # if pytest_output.return_code != 0:
    #     raise RuntimeError(f"Error running pytest: {pytest_output.stderr}, {pytest_output.stdout}")

    # Regular expression to match the summary line of pytest output
    # Example: "3 passed, 2 failed in 0.50 seconds"
    summary_regex = re.compile(r"(\d+) passed|(\d+) failed")

    passed_tests, failed_tests, coverage = 0, 0, 0.0

    # Search for the summary line in the pytest output
    matches = summary_regex.findall(pytest_output.stdout)
    for passed, failed in matches:
        if passed:
            passed_tests += int(passed)
        if failed:
            failed_tests += int(failed)

    # Regular expression to match the coverage percentage
    coverage_regex = re.compile(r"Total coverage: (\d+\.\d+)%")
    # Match and capture coverage percentage
    coverage_match = coverage_regex.search(pytest_output.stdout)
    if coverage_match:
        coverage = float(coverage_match.group(1))
    return passed_tests, failed_tests, coverage, pytest_output


def invoke_pytest(tests_path: str) -> CommandResult:
    """
    Runs pytest.

    Args:
        tests_path (str): The path to the tests.

    Returns:
        CommandResult: The result of the command.
    """
    command_name = "pytest"
    arg_string = f"'{tests_path}'"

    # generic response.
    return safe_subprocess(command_name, arg_string)


if __name__ == "__main__":
    # Example usage
    # with change_directory("../../src/"):
    #     try:
    #         passed, failed = count_pytest_results("tests")
    #         print(f"MDM: Passed Tests: {passed}, Failed Tests: {failed}")
    #     except RuntimeError as e:
    #         print(str(e))
    def run() -> None:
        """Example code"""
        with change_directory("../../src/"):
            try:
                passed_tests, failed_tests, coverage, pytest_output = count_pytest_results(
                    "fish_tank", "tests", min_coverage=10
                )
                print(pytest_output.stdout)
                print(pytest_output.stderr)
                print(passed_tests, failed_tests, coverage)
            except RuntimeError as e:
                print(str(e))

    run()
