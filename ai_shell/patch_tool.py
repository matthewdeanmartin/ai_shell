"""
The primary editing tool: apply a unified (git) diff to files in the root folder.

LLMs are generally better at producing unified diffs than at line-editor scripts,
so this is the headline edit mechanism. The model still has to produce a valid
patch (correct line counts / context), so on success we optionally return the
patched file contents (`auto_cat`) — a clean exit is not proof the edit was right.
"""

import logging
import os
import subprocess  # nosec
import tempfile

from ai_shell.ai_logs.log_to_bash import log
from ai_shell.cat_tool import CatTool
from ai_shell.utils.config_manager import Config
from ai_shell.utils.read_fs import is_file_in_root_folder

logger = logging.getLogger(__name__)


class PatchTool:
    """Edit files by applying a unified (git) diff."""

    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the PatchTool with a root folder.

        Args:
            root_folder (str): The root folder for valid patchable files.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder: str = root_folder
        self.config = config
        self.auto_cat = config.get_flag("auto_cat", True)

    @log()
    def apply_git_patch(self, patch_content: str) -> str:
        """
        Apply a unified (git) diff to the files in the root folder.

        Args:
            patch_content (str): The content of the unified/git diff.

        Returns:
            str: A message indicating the patch applied, plus the patched file
                 contents when auto_cat is enabled.

        Raises:
            ValueError: If the patch targets a file outside the root folder.
            RuntimeError: If the patch application fails.
        """
        target_files = self._extract_files_from_patch(patch_content)
        if not target_files:
            raise ValueError("No target files found in patch. Is this a valid unified diff?")
        for file_name in target_files:
            if not is_file_in_root_folder(file_name, self.root_folder):
                raise ValueError(f"Patch targets '{file_name}' outside the root folder, which is not allowed.")

        # Write the patch to a temp file and let `git apply` do the work; it is
        # more forgiving of context offsets than an in-process strict apply.
        with tempfile.NamedTemporaryFile(suffix=".patch", delete=False) as tmp_patch:
            tmp_patch_name = tmp_patch.name
            tmp_patch.write(patch_content.encode("utf-8"))
            tmp_patch.flush()

        cmd = ["git", "apply", tmp_patch_name, "--reject", "--verbose"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=False)  # nosec
            logger.info("STDOUT:\n%s", result.stdout)
            logger.info("STDERR:\n%s", result.stderr)
            if result.returncode != 0:
                raise RuntimeError(f"Failed to apply patch: {result.stderr}")
        except subprocess.CalledProcessError as cpe:
            raise RuntimeError(f"Failed to apply patch: {cpe.stderr or cpe.stdout}") from cpe
        finally:
            try:
                os.remove(tmp_patch_name)
            except OSError:
                pass

        if self.auto_cat:
            existing = [f for f in sorted(target_files) if os.path.exists(f)]
            if existing:
                contents = CatTool(self.root_folder, self.config).cat_markdown(existing)
                return (
                    "Patch applied without exception, please verify the contents below are what you intended.\n\n"
                    f"{contents}"
                )
        return "Patch applied without exception, please verify by other means to see if it was successful."

    def _extract_files_from_patch(self, patch_content: str) -> set[str]:
        """
        Extract target file names from the patch content.

        Args:
            patch_content (str): The content of the unified/git diff.

        Returns:
            set[str]: The set of file names the patch touches.
        """
        file_names = set()
        for line in patch_content.split("\n"):
            if line.startswith("diff --git "):
                # `diff --git a/path b/path`
                for token in line.split()[2:]:
                    file_names.add(self._strip_ab_prefix(token))
            elif line.startswith("--- ") or line.startswith("+++ "):
                parts = line.split()
                if len(parts) > 1 and parts[1] != "/dev/null":
                    file_names.add(self._strip_ab_prefix(parts[1]))
        return file_names

    @staticmethod
    def _strip_ab_prefix(file_name: str) -> str:
        """Strip a leading ``a/`` or ``b/`` from a diff path."""
        if file_name.startswith(("a/", "b/")):
            return file_name[2:]
        return file_name
