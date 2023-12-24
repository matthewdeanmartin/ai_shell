import subprocess
from unittest.mock import patch

import pytest

from ai_shell.patch_tool import PatchTool


def test_apply_git_patch_success(tmp_path):
    # Create a dummy patch content
    patch_content = "diff --git a/file.txt b/file.txt\nnew file mode 100644\nindex 0000000..e69de29"

    # Initialize PatchTool with the temporary directory
    tool = PatchTool(str(tmp_path))

    # Mock subprocess.run to simulate successful git apply
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="Patch applied successfully.", stderr=""
        )

        # Call apply_git_patch and assert success
        message = tool.apply_git_patch(patch_content)
        assert message == "Patch applied without exception, please verify by other means to see if it was successful."


def test_apply_git_patch_failure(tmp_path):
    # Create a dummy patch content
    patch_content = "invalid patch format"

    # Initialize PatchTool with the temporary directory
    tool = PatchTool(str(tmp_path))

    # Mock subprocess.run to simulate a failed git apply
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="patch failed")

        # Call apply_git_patch and expect a RuntimeError
        with pytest.raises(RuntimeError) as excinfo:
            tool.apply_git_patch(patch_content)
        assert "Failed to apply patch" in str(excinfo.value)


def test_extract_files_from_patch():
    tool = PatchTool("dummy_root_folder")

    # Example patch content
    patch_content = """
diff --git a/file1.txt b/file1.txt
new file mode 100644
index 0000000..e69de29
--- a/file1.txt
+++ b/file1.txt
diff --git a/dir/file2.txt b/dir/file2.txt
new file mode 100644
index 0000000..e69de29
--- a/dir/file2.txt
+++ b/dir/file2.txt
"""

    expected_files = {"file1.txt", "dir/file2.txt"}
    extracted_files = tool._extract_files_from_patch(patch_content)

    assert extracted_files == expected_files, "Extracted files do not match expected files"
