import os
from pathlib import Path
from typing import Optional

import pytest

from ai_shell import change_directory
from ai_todo import TaskManager
from ai_todo.models import Task, Work


@pytest.fixture
def task_manager(tmp_path: Path):
    # Set the current working directory to tmp_path
    with change_directory(str(tmp_path)):
        yield TaskManager(str(tmp_path), ["Alice", "Bob"])


def test_init(task_manager: TaskManager):
    # Test that the Work object is correctly initialized
    assert isinstance(task_manager.work, Work), "work should be an instance of Work"

    # Check if the completed and incomplete files are correctly set
    expected_completed_file = "todo_completed.toml"
    expected_incomplete_file = "todo_incomplete.toml"

    assert task_manager.work.completed.file_path.endswith(
        expected_completed_file
    ), "completed_file should be set to todo_completed.toml"
    assert task_manager.work.incomplete.file_path.endswith(
        expected_incomplete_file
    ), "incomplete_file should be set to todo_incomplete.toml"

    # Verify that the files are in the current working directory
    cwd = os.path.abspath(os.getcwd())
    assert task_manager.work.completed.file_path.startswith(
        cwd
    ), "completed_file should be in the current working directory"
    assert task_manager.work.incomplete.file_path.startswith(
        cwd
    ), "incomplete_file should be in the current working directory"

    # Check valid assignees
    assert task_manager.work.valid_assignees == ["Alice", "Bob"], "valid_assignees should be correctly set"


def add_sample_tasks(task_manager: TaskManager):
    tasks = [
        Task("Task 1", "Description 1", False, "Category 1", "CodeRef1", "Alice"),
        Task("Task 2", "Description 2", False, "Category 2", "CodeRef2", "Bob"),
        Task("Task 3", "Description 3", False, "Category 3", "CodeRef3", None),
    ]
    for task in tasks:
        task_manager.add_task(task.title, task.description, task.category, task.source_code_ref, task.assignee)


@pytest.mark.parametrize("assignee, expected_count", [("Alice", 1), ("Bob", 1), ("Charlie", 0), (None, 0)])
def test_query_by_assignee(task_manager: TaskManager, assignee: Optional[str], expected_count: int):
    add_sample_tasks(task_manager)

    result = task_manager.query_by_assignee(assignee)
    if expected_count > 0:
        assert f"Total Tasks: {expected_count}" in result, f"Expected {expected_count} tasks for assignee {assignee}"
    else:
        assert (
            result == "Invalid assignee. These are valid ['Alice', 'Bob']"
        ), "Result should be an empty string for no tasks or invalid assignee"


def add_sample_tasks_for_search(task_manager: TaskManager):
    tasks = [
        Task("Task Alpha", "Description 1", False, "Category 1", "CodeRef1", "Alice"),
        Task("Task Beta", "Description 2", False, "Category 2", "CodeRef2", "Bob"),
        Task("Task Gamma", "Description 3", False, "Category 3", "CodeRef3", None),
    ]
    for task in tasks:
        task_manager.add_task(task.title, task.description, task.category, task.source_code_ref, task.assignee)


@pytest.mark.parametrize(
    "keyword, expected_titles",
    [
        ("Alpha", ["Task Alpha"]),
        ("Delta", []),
        ("", ["Task Alpha", "Task Beta", "Task Gamma"]),  # Blank query should return all tasks
    ],
)
def test_query_by_title_keyword(task_manager: TaskManager, keyword: str, expected_titles: list[str]):
    add_sample_tasks_for_search(task_manager)

    result = task_manager.query_by_title_keyword(keyword)
    for title in expected_titles:
        assert title in result, f"Task with title '{title}' should be in the results for keyword '{keyword}'"

    if not expected_titles:
        assert (
            "Total Matching Tasks: 0" in result
        ), "Result should be an empty string for a keyword with no matching tasks"


def test_add_task(task_manager: TaskManager):
    # Test adding a valid task
    task_manager.add_task("Task 1", "Description 1", "Category 1", "CodeRef1", "Alice")
    assert "Task 1" in task_manager.work.incomplete.tasks, "Task 1 should be in incomplete tasks"
    task_1 = task_manager.work.incomplete.tasks["Task 1"]
    assert task_1.title == "Task 1", "Title of task 1 should be 'Task 1'"
    assert task_1.description == "Description 1", "Description of task 1 should be 'Description 1'"
    assert task_1.category == "Category 1", "Category of task 1 should be 'Category 1'"
    assert task_1.source_code_ref == "CodeRef1", "Source code ref of task 1 should be 'CodeRef1'"
    assert task_1.assignee == "Alice", "Assignee of task 1 should be 'Alice'"

    # Test adding a task with an invalid assignee
    with pytest.raises(ValueError):  # Assuming your code raises a ValueError for invalid assignee
        task_manager.add_task("Task 2", "Description 2", "Category 2", "CodeRef2", "Charlie")

    # Test adding a task with missing fields
    # with pytest.raises(TypeError):  # Assuming your code raises a TypeError for missing arguments
    #     task_manager.add_task("Task 3")  # mypy should catch this?


def add_sample_done_task(task_manager: TaskManager, title: str, assignee: str):
    task_manager.add_task(title, "Sample Description", "Sample Category", "Sample CodeRef", assignee)


def test_finish_task(task_manager: TaskManager):
    # Add a sample task and finish it
    task_title = "Sample Task"
    add_sample_done_task(task_manager, task_title, "Alice")
    task_manager.finish_task(task_title)
    assert task_manager.work.completed.tasks[task_title].done_status, "The task should be marked as completed"

    # Check if the task is moved to completed tasks or handled appropriately
    # This assertion depends on the implementation of archive_completed_tasks()
    # Example:
    # assert task_title not in task_manager.work.incomplete.tasks, \
    #     "Finished task should be removed from incomplete tasks"
    # assert task_title in task_manager.work.completed.tasks, \
    #     "Finished task should be added to completed tasks"

    # Test finishing a task that does not exist
    non_existent_task_title = "Non-existent Task"
    with pytest.raises(KeyError):
        task_manager.finish_task(non_existent_task_title)
