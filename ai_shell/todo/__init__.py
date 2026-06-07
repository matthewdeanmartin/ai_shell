"""A tiny task store for agents.

- python interface
- Markdown + YAML frontmatter data store (the convention other agents read)
- simpler than Jira
- pairs each task with acceptance criteria (`done_when`) for the goal loop
"""

from ai_shell.todo.public_api import TaskManager

__all__ = ["TaskManager"]
