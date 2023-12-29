"""
Apply patch with unidiff instead of Git
"""
import unidiff

from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log


class DiffTool:
    """Work with file diffs using unidiff library."""

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
    def apply_git_patch(self, diff_string: str, target_file: str) -> str:
        """
        Applies a git diff patch to a specific file.

        Args:
            diff_string (str): The diff string obtained from git diff.
            target_file (str): The name of the file to which the diff will be applied.

        Returns:
            str: status message or result of change.
        """
        # Create a PatchSet from the diff string
        # was diff_string.splitlines(keepends=True)...
        patch_set = unidiff.PatchSet(diff_string)

        # Find the specific patch for the target file
        target_patch = None
        for patch in patch_set:
            if patch.target_file in (f"a/{target_file}", f"b/{target_file}"):
                target_patch = patch
                break

        if not target_patch:
            return f"No patch found for {target_file}"

        # Apply the patch
        patched_file = target_patch.apply()

        # Write the patched content back to the file
        with open(target_file, "w", encoding="utf-8") as file:
            file.writelines(patched_file)

        if self.auto_cat:
            with open(target_file, encoding="utf-8") as file:
                return "File after patching: \n\n" + file.read()
        return "No errors raised during application of patch"


if __name__ == "__main__":

    def run() -> None:
        """Example"""
        diff_string = "..."  # Replace with your actual diff string
        target_file = "path/to/your/target/file.ext"  # Replace with your actual target file path
        diff_tool = DiffTool(".", Config(".."))
        result = diff_tool.apply_git_patch(diff_string, target_file)
        print("Patch applied without error, please verify by viewing file." if result else "Failed to apply patch")

    run()
