import os
import re
from dataclasses import asdict, dataclass
from typing import Optional

import toml


@dataclass
class Task:
    title: str
    description: str
    done_status: bool
    category: str
    source_code_ref: str
    assignee: Optional[str] = None


@dataclass
class Todos:
    tasks: dict[str, Task]
    file_path: str
    valid_assignees: list[str]

    def __post_init__(self):
        self.tasks = {}  # Initialize the tasks dictionary

    def load_tasks(self):
        if os.path.exists(self.file_path):
            data = toml.load(self.file_path)
            for task_data in data.get("tasks", []):
                task = Task(**task_data)
                self.tasks[task.title] = task

    def save_tasks(self):
        with open(self.file_path, "w") as file:
            toml.dump({"tasks": [asdict(task) for task in self.tasks.values()]}, file)

    def add_task(self, new_task: Task):
        if new_task.title in self.tasks:
            raise ValueError(f"A task with the title '{new_task.title}' already exists.")
        self.tasks[new_task.title] = new_task
        self.save_tasks()

    def remove_task(self, title: str):
        if title in self.tasks:
            del self.tasks[title]
            self.save_tasks()
        else:
            raise KeyError(f"No task found with the title '{title}'.")

    def query_tasks_by_assignee(self, assignee_name: str):
        if assignee_name not in self.valid_assignees:
            raise ValueError(f"Invalid assignee. These are valid {self.valid_assignees}")
        return [task for task in self.tasks.values() if task.assignee == assignee_name]

    def query_tasks(self, pattern: str):
        matching_tasks = []
        for _title, task in self.tasks.items():
            if re.search(pattern, task.title) or re.search(pattern, task.description):
                matching_tasks.append(task)
        return matching_tasks


@dataclass
class Work:
    completed: Todos
    incomplete: Todos

    def __init__(self, completed_file: str, incomplete_file: str, valid_assignee: list[str]):
        self.completed = Todos({}, completed_file, valid_assignee)
        self.incomplete = Todos({}, incomplete_file, valid_assignee)
        self.completed.load_tasks()
        self.incomplete.load_tasks()
        self.valid_assignees = valid_assignee

    def archive_completed_tasks(self):
        titles_to_archive = [title for title, task in self.incomplete.tasks.items() if task.done_status]

        for title in titles_to_archive:
            # Move the task from incomplete to completed
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


if __name__ == "__main__":

    def run() -> None:
        """Example"""
        assginees = ["Developer", "Tester", "Documenter", "Code Reviewer"]
        work = Work("completed_tasks.toml", "incomplete_tasks.toml", assginees)

        # Example of adding a new task
        new_task = Task("New Feature", "Implement XYZ", False, "feature", "feature.py:30-45")
        work.incomplete.add_task(new_task)
        work.incomplete.save_tasks()

        new_task = Task("New Feature", "Implement ABC", False, "feature", "feature.py:30-45")
        work.incomplete.add_task(new_task)
        work.incomplete.save_tasks()

        xyz = work.incomplete.query_tasks("XYZ")
        xyz[0].done_status = True
        work.archive_completed_tasks()

    run()
