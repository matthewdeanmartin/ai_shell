"""
Bot frequently does lists in 3 different ways.
"""
import csv
from io import StringIO
from typing import Union


def convert_to_list(possible_list: Union[str, list[str]]) -> list[str]:
    """
    Convert a string to a list if it isn't already a list.

    Args:
        possible_list (Union[str, list[str]]): A string or list.

    Returns:
        A list.

    Examples:
        >>> convert_to_list("a,b,c")
        ['a', 'b', 'c']
        >>> convert_to_list(["a", "b", "c"])
        ['a', 'b', 'c']
        >>> convert_to_list("")
        []
    """
    if possible_list == "" or possible_list is None:
        # Degenerate case.
        return []
    if isinstance(possible_list, str):
        # Use csv.reader to handle complex cases
        # StringIO is used to turn the string into a file-like object
        reader = csv.reader(StringIO(possible_list))
        for row in reader:
            # Assuming there is only one row in the CSV string
            return row
    elif isinstance(possible_list, list):
        return possible_list
    raise TypeError(f"This list of strings is of invalid type: {possible_list}")
