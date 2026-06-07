"""
Task storage as Markdown with YAML frontmatter.

Each task is a Markdown document: a YAML frontmatter block (the structured fields)
followed by the description as the body. Files hold one or more such documents
separated by ``---`` fences, so they are readable by humans and by other agents
that already understand the Markdown-with-frontmatter convention — not a private
format.
"""

import os
import re
from dataclasses import dataclass, field

import yaml


@dataclass
class Task:
    """A unit of work.

    ``done_when`` is the acceptance criteria: how a bot (or human) knows the task
    is actually finished. It is what makes the "verify the bot did the one thing"
    loop possible.
    """

    title: str
    description: str
    done_status: bool
    category: str
    source_code_ref: str
    assignee: str | None = None
    done_when: str = ""


def _task_to_markdown(task: Task) -> str:
    """Render one task as a frontmatter block plus body."""
    front = {
        "title": task.title,
        "status": "done" if task.done_status else "todo",
        "category": task.category,
        "assignee": task.assignee,
        "source_code_ref": task.source_code_ref,
        "done_when": task.done_when,
    }
    front_yaml = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{front_yaml}\n---\n{task.description}\n"


def _parse_markdown(text: str) -> list[Task]:
    """Parse a Markdown file of frontmatter blocks into tasks."""
    tasks: list[Task] = []
    # Split into "--- frontmatter --- body" records.
    pattern = re.compile(r"---\n(.*?)\n---\n(.*?)(?=\n---\n|\Z)", re.DOTALL)
    for front_text, body in pattern.findall(text):
        front = yaml.safe_load(front_text) or {}
        tasks.append(
            Task(
                title=front.get("title", ""),
                description=body.strip(),
                done_status=front.get("status") == "done",
                category=front.get("category", ""),
                source_code_ref=front.get("source_code_ref", ""),
                assignee=front.get("assignee"),
                done_when=front.get("done_when", "") or "",
            )
        )
    return tasks


@dataclass
class Todos:
    """A collection of tasks backed by a single Markdown file."""

    tasks: dict[str, Task]
    file_path: str
    valid_assignees: list[str]

    def __post_init__(self) -> None:
        self.tasks = {}  # Initialize the tasks dictionary

    def load_tasks(self) -> None:
        if os.path.exists(self.file_path):
            with open(self.file_path, encoding="utf-8") as file:
                for task in _parse_markdown(file.read()):
                    self.tasks[task.title] = task

    def save_tasks(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(_task_to_markdown(task) for task in self.tasks.values()))

    def add_task(self, new_task: Task) -> None:
        if new_task.title in self.tasks:
            raise ValueError(f"A task with the title '{new_task.title}' already exists.")
        self.tasks[new_task.title] = new_task
        self.save_tasks()

    def remove_task(self, title: str) -> None:
        if title in self.tasks:
            del self.tasks[title]
            self.save_tasks()
        else:
            raise KeyError(f"No task found with the title '{title}'.")

    def query_tasks_by_assignee(self, assignee_name: str) -> list[Task]:
        if assignee_name not in self.valid_assignees:
            raise ValueError(f"Invalid assignee. These are valid {self.valid_assignees}")
        return [task for task in self.tasks.values() if task.assignee == assignee_name]

    def query_tasks(self, pattern: str) -> list[Task]:
        matching_tasks = []
        for _title, task in self.tasks.items():
            if re.search(pattern, task.title) or re.search(pattern, task.description):
                matching_tasks.append(task)
        return matching_tasks


@dataclass
class Work:
    """Incomplete and completed task stores, with archival between them."""

    completed: Todos = field(init=False)
    incomplete: Todos = field(init=False)

    def __init__(self, completed_file: str, incomplete_file: str, valid_assignee: list[str]):
        self.completed = Todos({}, completed_file, valid_assignee)
        self.incomplete = Todos({}, incomplete_file, valid_assignee)
        self.completed.load_tasks()
        self.incomplete.load_tasks()
        self.valid_assignees = valid_assignee

    def archive_completed_tasks(self) -> None:
        titles_to_archive = [title for title, task in self.incomplete.tasks.items() if task.done_status]

        for title in titles_to_archive:
            self.completed.tasks[title] = self.incomplete.tasks[title]
            del self.incomplete.tasks[title]

        self.completed.save_tasks()
        self.incomplete.save_tasks()

    def get_stats(self) -> str:
        """Summary of tasks"""
        return (
            f"Completed tasks: {len(self.completed.tasks)}\n"
            f"Incomplete tasks: {len(self.incomplete.tasks)}\n"
            f"Total tasks: {len(self.completed.tasks) + len(self.incomplete.tasks)}"
        )

    def get_stats_numeric(self) -> dict[str, int]:
        """Summary of stats in dictionary form"""
        return {
            "Completed tasks": len(self.completed.tasks),
            "Incomplete tasks": len(self.incomplete.tasks),
            "Total tasks": len(self.completed.tasks) + len(self.incomplete.tasks),
        }
