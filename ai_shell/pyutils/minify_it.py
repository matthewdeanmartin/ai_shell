"""
Credits: phpdude Github Gist as covered by Github's Terms of Service.
https://gist.github.com/phpdude/1ae6f19de213d66286c8183e9e3b9ec1
"""
import ast
import re

import astor

# TODO: Support whitespace reduction, e.g. 4 to 2 spaces


def strip_comments_docstrings(source: str) -> str:
    """Return a string of Python source code with comments and docstrings stripped.

    Args:
        source (str): The Python source code as a string.

    Returns:
        str: The Python source code with comments and docstrings removed.
    """
    parsed = ast.parse(source)

    for node in ast.walk(parsed):
        # let's work only on functions & classes definitions
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
            continue

        if not node.body:
            continue

        if not isinstance(node.body[0], ast.Expr):
            continue

        if not hasattr(node.body[0], "value") or not isinstance(node.body[0].value, ast.Str):
            continue

        # Uncomment lines below if you want print what and where we are removing
        # print(node)
        # if "comment" in node.body[0].value.s:
        #     print(node.body[0].value.s)

        node.body = node.body[1:]

    return astor.to_source(parsed)


def strip_docstrings_with_regex(source_code: str) -> str:
    """
    Strip docstrings from a given Python source code using regular expressions.

    Credit ChatGPT.
    Args:
        source_code (str): The Python source code as a string.

    Returns:
        str: The Python source code with docstrings removed.
    """
    # Regular expression pattern for docstrings
    pattern = r"(\"\"\"[\s\S]*?\"\"\"|\'\'\'[\s\S]*?\'\'\')"

    # Removing docstrings using the regular expression
    return re.sub(pattern, "", source_code, flags=re.MULTILINE)
