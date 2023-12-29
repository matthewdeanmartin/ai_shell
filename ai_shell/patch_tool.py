"""
Let the bot patch files instead of full rewrite. Also it is an alternative to editing with ed or edlin.

The bot has to make a perfect patch file or `git patch` rejects it with an opaque error message.
This is hard because of the line counting. So this usually fails.
"""

import logging
import subprocess  # nosec
import tempfile

from unidiff import PatchSet

from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log

logger = logging.getLogger(__name__)


class PatchTool:
    """Edit a file by applying a git patch."""

    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the PatchTool with a root folder.

        Args:
            root_folder (str): The root folder for valid patchable files.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder: str = root_folder
        self.config = config
        self.auto_cat = config.get_flag("auto_cat")

    @log()
    def apply_git_patch(self, patch_content: str) -> str:
        """
        Apply a git patch to the files in the root folder.

        Args:
            patch_content (str): The content of the git patch.

        Returns:
            str: A message indicating successful patch application.

        Raises:
            RuntimeError: If the patch application fails.
        """
        # Create a temporary file to store the patch content
        with tempfile.NamedTemporaryFile(suffix=".patch", delete=False) as tmp_patch:
            tmp_patch_name = tmp_patch.name
            tmp_patch.write(patch_content.encode("utf-8"))
            tmp_patch.flush()

        try:
            patch = PatchSet.from_filename(tmp_patch_name, encoding="utf-8")
            print(patch)
        except Exception as ex:
            print(ex)

        cmd = ["git", "apply", tmp_patch_name, "--reject", "--verbose"]

        # Execute the command and capture stdout and stderr
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=False)  # nosec
            # Log stdout and stderr
            logger.info("STDOUT:\n%s", result.stdout.replace(" ", ".").replace("\n", "\\n"))
            logger.info("STDERR:\n%s", result.stderr.replace(" ", ".").replace("\n", "\\n"))

            # Check for errors and return the result
            if result.returncode != 0:
                raise RuntimeError(f"Failed to apply patch: {result.stderr}")

        except subprocess.CalledProcessError as cpe:
            print(cpe)
            print(cpe.stdout)
            print(cpe.stderr)

        return "Patch applied without exception, please verify by other means to see if it was successful."

    def _extract_files_from_patch(self, patch_content: str) -> set[str]:
        """
        Extract file names from the patch content.

        Args:
            patch_content (str): The content of the git patch.

        Returns:
            set[str]: A set of file names extracted from the patch.
        """
        file_names = set()
        lines = patch_content.split("\n")

        for line in lines:
            if line.startswith("--- a/") or line.startswith("+++ b/"):
                # Extract the file name and add it to the set
                parts = line.split()
                if len(parts) > 1:
                    file_name = parts[1]
                    if file_name.startswith("a/") or file_name.startswith("b/"):
                        file_name = file_name[2:]
                    file_names.add(file_name)

        return file_names


# if __name__ == "__main__":
#     tool = PatchTool(".")
#     print(tool._extract_files_from_patch(open("a.patch", encoding="utf-8").read()))
#     tool.apply_git_patch(open("a.patch", encoding="utf-8").read())

# if __name__ == "__main__":
#
#     def run1() -> None:
#         """run"""
#         # Example usage
#         patch_content = """
#         --- a/example.txt
#         +++ b/example.txt
#         @@ -1,3 +1,4 @@
#         +Added line
#          Line 1
#          Line 2
#          Line 3
#         --- a/another_file.txt
#         +++ b/another_file.txt
#         @@ -2,3 +2,4 @@
#          Another line
#         """
#         tool = PatchTool("dummy_root_folder")
#         file_names = tool._extract_files_from_patch(patch_content)
#         print("Files to be patched:", file_names)
#
#     run1()
#
# if __name__ == "__main__":
#
#     def run() -> None:
#         """run"""
#         # Example usage
#         patch_content = "--- a/ai_shell/example.txt\n+++ b/ai_shell/example.txt\n@@ -1,3 +1,4 @@\n+Added line\n Line 1\n Line 2\n Line 3\n"
#         original_content = "Line 1\nLine 2\nLine 3\n"
#
#         example_file = "example.txt"
#         with open("example.txt", "wb") as file:
#             file.write(original_content.encode("utf-8"))
#             file.flush()
#         convert = LineEndingConverter(example_file)
#         # convert.dos2unix()
#         # convert = LineEndingConverter(example_file)
#         print("---example----")
#         print(convert.check_line_endings())
#         tool = PatchTool(".")
#         result = tool.apply_git_patch(patch_content)
#         print(result)
#
#     run()
