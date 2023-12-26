"""
Generate code for AI Shell using the docstrings as source data.

Currently, targets:
- CLI interface
- Toolkit
- JsonSchema dict
"""

from ai_shell.code_generate.generate_cli import generate_the_cli
from ai_shell.code_generate.generate_schema import generate_the_schema
from ai_shell.code_generate.generate_toolkit import generate_the_toolkit

__all__ = ["generate_the_schema", "generate_the_toolkit", "generate_the_cli"]
