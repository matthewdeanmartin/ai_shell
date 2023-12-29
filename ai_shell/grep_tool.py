"""
AI optimized grep tool
"""

import glob
import logging
import os.path
import re
from dataclasses import dataclass, field
from io import StringIO

from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log
from ai_shell.utils.read_fs import is_file_in_root_folder, remove_root_folder


@dataclass
class Match:
    """Represents a single match found in a file."""

    line_number: int
    line: str


@dataclass
class FileMatches:
    """Stores matches found in a single file."""

    filename: str
    found: list[Match] = field(default_factory=list)


@dataclass
class GrepResults:
    """Stores the results of a grep operation."""

    matches_found: int
    data: list[FileMatches] = field(default_factory=list)


logger = logging.getLogger(__name__)


class GrepTool:
    """A tool for searching files using regular expressions."""

    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the GrepTool with a root folder.

        Args:
            root_folder (str): The root folder to search within.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder: str = root_folder
        self.config = config
        self.auto_cat = config.get_flag("auto_cat")

    @log()
    def grep_markdown(
        self, regex: str, glob_pattern: str, skip_first_matches: int = -1, maximum_matches: int = -1
    ) -> str:
        """
        Search for lines matching a regular expression in files and returns markdown formatted results.

        Args:
            regex (str): A regular expression string to search for.
            glob_pattern (str): A glob pattern string to specify files.
            skip_first_matches (int): Number of initial matches to skip.
            maximum_matches (int): Maximum number of matches to return.

        Returns:
            str: Markdown formatted string of grep results.
        """
        results = self.grep(regex, glob_pattern, skip_first_matches, maximum_matches)
        matches_found = results.matches_found

        output = StringIO()
        for file_match in results.data:
            output.write(file_match.filename + "\n")
            for match in file_match.found:
                output.write(f"line {match.line_number}: {match.line}\n")
        output.write(
            f"{matches_found} matches found and {min(matches_found, maximum_matches) if maximum_matches != -1 else matches_found} displayed. "
            f"Skipped {skip_first_matches}\n"
        )
        output.seek(0)
        return output.read()

    @log()
    def grep(
        self,
        regex: str,
        glob_pattern: str,
        skip_first_matches: int = -1,
        maximum_matches_per_file: int = -1,
        maximum_matches_total: int = -1,
    ) -> GrepResults:
        """
        Search for lines matching a regular expression in files specified by a glob pattern.

        Args:
            regex (str): A regular expression string to search for.
            glob_pattern (str): A glob pattern string to specify files.
            skip_first_matches (int): Number of initial matches to skip.
            maximum_matches_per_file (int): Maximum number of matches to return for one file.
            maximum_matches_total (int): Maximum number of matches to return total.

        Returns:
            GrepResults: The results of the grep operation.
        """
        logger.info(
            f"grep --regex {regex} --glob_pattern {glob_pattern} "
            f"--skip_first_matches {skip_first_matches} "
            f"--maximum_matches_total {maximum_matches_total} "
            f"--maximum_matches_per_file {maximum_matches_per_file}"
        )
        pattern = re.compile(regex)
        matches_total = 0
        skip_count = 0 if skip_first_matches < 0 else skip_first_matches

        results = GrepResults(matches_found=-1)

        for filename in glob.glob(glob_pattern, root_dir=self.root_folder, recursive=True):
            matches_per_file = 0

            if not os.path.exists(filename):
                # What a hack
                open_path = self.root_folder + "/" + filename
            else:
                open_path = filename
            with open(open_path, encoding="utf-8") as file:
                if not is_file_in_root_folder(filename, self.root_folder):
                    continue
                line_number = 0
                for line in file:
                    if matches_per_file < maximum_matches_per_file or maximum_matches_per_file == -1:
                        line_number += 1
                        if pattern.search(line):
                            matches_total += 1
                            matches_per_file += 1

                            if matches_total <= (matches_total + skip_count) or matches_total == -1:
                                if (0 < skip_first_matches < matches_total) or skip_first_matches == -1:
                                    # This creates names like \..\..\..\ etc.
                                    minimal_filename = remove_root_folder(filename, self.root_folder)
                                    # avoid double count
                                    found = next((fm for fm in results.data if fm.filename == minimal_filename), None)
                                    if not found:
                                        found = FileMatches(filename=minimal_filename)
                                        results.data.append(found)

                                    found.found.append(Match(line_number=line_number, line=line.strip()))
        results.data = list(sorted(results.data, key=lambda x: x.filename))
        results.matches_found = matches_total
        return results


if __name__ == "__main__":
    tool = GrepTool(".", config=Config(".."))
    print(tool.grep(glob_pattern="*.py", regex="print\\(|logging", maximum_matches_per_file=1))
