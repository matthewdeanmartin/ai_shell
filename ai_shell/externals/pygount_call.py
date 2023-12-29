"""
Check for lines of code for when the bot blows away most of the file.
"""
from pygount import SourceAnalysis


def count_lines_of_code(file_path: str) -> SourceAnalysis:
    """
    Check the lines of code in a file. File must exist.
    Args:
        file_path (str): The path to the file.

    Returns:
        SourceAnalysis: The analysis of the file, including line counts.
    """
    return SourceAnalysis.from_file(file_path, "pygount", encoding="utf-8")


if __name__ == "__main__":
    print(count_lines_of_code(__file__))
