"""
Utility code for testing app via console.
"""
from typing import Any

import orjson


def pretty_console(result: Any) -> None:
    """
    Print result to console in a pretty way
    Args:
        result (Any): The result to print to console.
    """
    if isinstance(result, str):
        print(result)
    else:
        print(orjson.dumps(result, option=orjson.OPT_INDENT_2).decode())
        # json.dump(result, sys.stdout, indent=4, cls=LoosyGoosyEncoderForSlowJson)
