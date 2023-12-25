"""
Read source with tools that understand the stucture of python
"""
import ast
import inspect

import markpickle
import python_minifier


def minify(file_path: str) -> str:
    """Return the minimified source of a file"""
    with open(file_path, encoding="utf-8") as f:
        raw_text = f.read()
        return python_minifier.minify(raw_text)


def astify(file_path: str) -> str:
    """Return the ast of a file"""
    with open(file_path, encoding="utf-8") as f:
        raw_text = f.read()
        return ast.dump(ast.parse(raw_text), indent=4)


def get_source(_module_path: str, _function_name: str) -> str:
    """Takes file system path to module and name of function as string, Return source code"""
    # TODO: use importlib to import markpickle from "e:/github/src/"
    return inspect.getsource(markpickle.split_file)
