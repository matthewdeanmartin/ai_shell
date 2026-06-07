import subprocess
from unittest.mock import patch

import pytest

from ai_shell.patch_tool import PatchTool
from tests.util import config_for_tests


def test_apply_git_patch_success(tmp_path):
    # A real-ish unified diff header so file extraction + jail check pass.
    patch_content = "diff --git a/file.txt b/file.txt\nnew file mode 100644\nindex 0000000..e69de29"

    tool = PatchTool(str(tmp_path), config=config_for_tests())
    tool.auto_cat = False  # don't try to cat a file that the mock didn't create

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="Patch applied successfully.", stderr=""
        )
        message = tool.apply_git_patch(patch_content)
        assert "Patch applied without exception" in message


def test_apply_git_patch_failure(tmp_path):
    patch_content = "diff --git a/file.txt b/file.txt\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1 @@\n-a\n+b\n"

    tool = PatchTool(str(tmp_path), config=config_for_tests())

    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=["git", "apply"], output="", stderr="patch failed"
        )
        with pytest.raises(RuntimeError) as excinfo:
            tool.apply_git_patch(patch_content)
        assert "Failed to apply patch" in str(excinfo.value)


def test_apply_git_patch_outside_root_rejected(tmp_path):
    # A patch targeting a parent-directory path must be rejected before any git call.
    root = tmp_path / "project"
    root.mkdir()
    tool = PatchTool(str(root), config=config_for_tests())
    sibling = (tmp_path / "secret.txt").resolve().as_posix()
    patch_content = f"diff --git a/{sibling} b/{sibling}\n--- a/{sibling}\n+++ b/{sibling}\n"
    with pytest.raises(ValueError) as excinfo:
        tool.apply_git_patch(patch_content)
    assert "outside the root folder" in str(excinfo.value)


def test_apply_git_patch_no_targets_rejected(tmp_path):
    tool = PatchTool(str(tmp_path), config=config_for_tests())
    with pytest.raises(ValueError) as excinfo:
        tool.apply_git_patch("this is not a diff at all")
    assert "No target files" in str(excinfo.value)


def test_extract_files_from_patch():
    tool = PatchTool("dummy_root_folder", config=config_for_tests())

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
