"""
Utility code for testing app via console.
"""
import json
import sys
from typing import Any

from ai_shell.utils.json_utils import LoosyGoosyEncoder


def pretty_console(result: Any) -> None:
    """
    Print result to console in a pretty way
    Args:
        result (Any): The result to print to console.
    """
    if isinstance(result, str):
        print(result)
    else:
        json.dump(result, sys.stdout, indent=4, cls=LoosyGoosyEncoder)
