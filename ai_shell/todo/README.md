# ai_shell.todo

A tiny task store for agents. Models struggle with a prompt that has too much
going on at once; this lets you split work into items, hand a bot **one at a
time**, and check whether it did that one thing before moving on.

## The "goal function is a work queue" pattern

The reason this exists: pair each task with **acceptance criteria** (`done_when`),
then loop — give the bot one task, run the check in `done_when`, and only advance
when it passes. The task list *is* the agent's goal queue.

## Storage: Markdown with YAML frontmatter

Tasks are stored as Markdown documents with a YAML frontmatter block, in `TODO.md`
(incomplete) and `TODO_done.md` (archived). This is the convention other agents
already understand — not a private format — so the files are useful on their own.

```markdown
---
title: Fix off-by-one in pager
status: todo
category: bug
assignee: Developer
source_code_ref: ai_shell/head_tail_tool.py:42
done_when: tests/test_head_tail.py passes and tail returns N lines
---
The `tail` path returns N-1 lines when byte_count is unset.
```

## API

```python
from ai_shell.todo.public_api import TaskManager

tm = TaskManager(root_folder=".", valid_assignees=["Developer", "Tester"])
tm.add_task(
    title="Fix off-by-one in pager",
    description="tail returns N-1 lines",
    category="bug",
    source_code_ref="ai_shell/head_tail_tool.py:42",
    assignee="Developer",
    done_when="tests/test_head_tail.py passes",
)
print(tm.query_by_assignee("Developer"))
tm.finish_task("Fix off-by-one in pager")  # archives to TODO_done.md
```

The same operations are exposed to models as the `add_todo`, `remove_todo`,
`query_todos_by_assignee`, `query_todos_by_regex`, and `list_valid_assignees`
tools.
