"""Helpers for optional pygount-based line counting."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygount import SourceAnalysis


def count_lines_of_code(file_path: str) -> "SourceAnalysis":
    """
    Check the lines of code in a file. File must exist.
    Args:
        file_path (str): The path to the file.

    Returns:
        SourceAnalysis: The analysis of the file, including line counts.
    """
    try:
        from pygount import SourceAnalysis
    except ImportError as exc:
        raise RuntimeError(
            "count_lines_of_code requires pygount. Install ai_shell[checkers] or the pygount package."
        ) from exc

    return SourceAnalysis.from_file(file_path, "pygount", encoding="utf-8")


if __name__ == "__main__":
    print(count_lines_of_code(__file__))
