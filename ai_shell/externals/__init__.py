"""
Wrappers for external CLI tools that require subprocess calls.
"""
from ai_shell.externals.black_call import invoke_black
from ai_shell.externals.mypy_call import invoke_mypy
from ai_shell.externals.pylint_call import invoke_pylint
from ai_shell.externals.pytest_call import invoke_pytest
from ai_shell.externals.ruff_call import invoke_ruff

__all__ = [
    "invoke_black",
    "invoke_mypy",
    "invoke_pylint",
    "invoke_pytest",
    "invoke_ruff",
]
