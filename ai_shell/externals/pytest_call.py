import re

from ai_shell.externals.subprocess_utils import safe_subprocess


def count_pytest_results(module: str):
    # Run pytest using safe_subprocess
    pytest_output = safe_subprocess("pytest", f"'{module}'", markdown=False)

    # Check if there was an error running pytest
    if pytest_output.return_code != 0:
        raise RuntimeError(f"Error running pytest: {pytest_output.stderr}")

    # Regular expression to match the summary line of pytest output
    # Example: "3 passed, 2 failed in 0.50 seconds"
    # summary_regex = re.compile(r'(\d+) passed, (\d+) failed')
    summary_regex = re.compile(r"(\d+) passed|(\d+) failed")

    passed_tests, failed_tests = 0, 0
    # Search for the summary line in the pytest output
    matches = summary_regex.findall(pytest_output.stdout)
    for passed, failed in matches:
        if passed:
            passed_tests += int(passed)
        if failed:
            failed_tests += int(failed)
    return passed_tests, failed_tests


# if __name__ == '__main__':
#     # Example usage
#     with change_directory("../.."):
#         try:
#             passed, failed = count_pytest_results("fish_tank")
#             print(f"MDM: Passed Tests: {passed}, Failed Tests: {failed}")
#         except RuntimeError as e:
#             print(str(e))
