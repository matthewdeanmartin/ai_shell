"""
Apply patch with unidiff instead of Git
"""
import unidiff

from ai_shell.utils.logging_utils import log


@log()
def apply_git_patch(diff_string: str, target_file: str):
    """
    Applies a git diff patch to a specific file.

    Args:
        diff_string (str): The diff string obtained from git diff.
        target_file (str): The name of the file to which the diff will be applied.

    Returns:
        bool: True if the patch was successfully applied, False otherwise.
    """
    # Create a PatchSet from the diff string
    patch_set = unidiff.PatchSet(diff_string.splitlines(keepends=True))

    # Find the specific patch for the target file
    target_patch = None
    for patch in patch_set:
        if patch.target_file in (f"a/{target_file}", f"b/{target_file}"):
            target_patch = patch
            break

    if not target_patch:
        print(f"No patch found for {target_file}")
        return False

    # Apply the patch
    patched_file = target_patch.apply()

    # Write the patched content back to the file
    with open(target_file, "w", encoding="utf-8") as file:
        file.writelines(patched_file)

    return True


if __name__ == "__main__":

    def run() -> None:
        """Example"""
        diff_string = "..."  # Replace with your actual diff string
        target_file = "path/to/your/target/file.ext"  # Replace with your actual target file path
        result = apply_git_patch(diff_string, target_file)
        print("Patch applied without error, please verify by viewing file." if result else "Failed to apply patch")

    run()
