import os
from typing import Optional

from ai_todo.models import Task, Work
from ai_todo.views import assigned_incomplete_tasks_to_markdown, search_results_to_markdown


class TaskManager:
    def __init__(self, root_folder: str, valid_assignees: list[str]):
        # put these into the pwd folder, not root_folder.
        completed_file = os.path.abspath("todo_completed.toml")
        incomplete_file = os.path.abspath("todo_incomplete.toml")
        self.work = Work(completed_file, incomplete_file, valid_assignees)
        if not valid_assignees:
            raise ValueError("Need at least 1 assignee")
        self.valid_assignees = valid_assignees

    def query_by_assignee(self, assignee_name: str) -> str:
        try:
            results = self.work.incomplete.query_tasks_by_assignee(assignee_name)
        except ValueError as value:
            return str(value)

        return assigned_incomplete_tasks_to_markdown(assignee_name, results)

    def query_by_title_keyword(self, keyword: str) -> str:
        results = self.work.incomplete.query_tasks(keyword)
        return search_results_to_markdown(keyword, results)

    def add_task(
        self, title: str, description: str, category: str, source_code_ref: str, assignee: Optional[str] = None
    ) -> None:
        if assignee not in self.valid_assignees and assignee is not None:
            raise ValueError(f"Invalid assignee. These are valid {self.valid_assignees}")
        new_task = Task(title, description, False, category, source_code_ref, assignee)
        self.work.incomplete.add_task(new_task)
        self.work.incomplete.save_tasks()  # Save after adding task

    def finish_task(self, title: str) -> None:
        if title in self.work.incomplete.tasks:
            self.work.incomplete.tasks[title].done_status = True
            self.work.incomplete.save_tasks()  # Save after finishing task
            self.work.archive_completed_tasks()  # Archive if necessary
            self.work.completed.save_tasks()  # Save changes in completed tasks
        else:
            raise KeyError(f"Task with title '{title}' not found in incomplete tasks.")

    def get_stats(self) -> str:
        return self.work.get_stats()

    def get_stats_numeric(self) -> dict[str, int]:
        return self.work.get_stats_numeric()
