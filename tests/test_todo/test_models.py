import re

from ai_shell.utils.read_fs import temporary_change_dir
from ai_todo.models import Task, Todos, Work  # Replace 'your_module' with the actual module name


def test_add_task(tmp_path):
    with temporary_change_dir(str(tmp_path)):
        tasks_file = tmp_path / "tasks.toml"
        todos = Todos({}, str(tasks_file), ["Developer", "Tester"])

        task = Task("Task 1", "Description", False, "bug", "file.py:10", "Developer")
        todos.add_task(task)

        assert "Task 1" in todos.tasks
        assert todos.tasks["Task 1"].assignee == "Developer"


def test_remove_task(tmp_path):
    with temporary_change_dir(str(tmp_path)):
        tasks_file = tmp_path / "tasks.toml"
        todos = Todos({}, str(tasks_file), ["Developer", "Tester"])

        task = Task("Task 1", "Description", False, "bug", "file.py:10", "Developer")
        todos.add_task(task)
        todos.remove_task("Task 1")

        assert "Task 1" not in todos.tasks


def test_archive_completed_tasks(tmp_path):
    with temporary_change_dir(str(tmp_path)):
        completed_file = tmp_path / "completed.toml"
        incomplete_file = tmp_path / "incomplete.toml"
        work = Work(str(completed_file), str(incomplete_file), ["Developer", "Tester"])

        task = Task("Task 1", "Description", True, "bug", "file.py:10", "Developer")
        work.incomplete.add_task(task)
        work.archive_completed_tasks()

        assert "Task 1" not in work.incomplete.tasks
        assert "Task 1" in work.completed.tasks


def test_query_tasks_by_assignee(tmp_path):
    with temporary_change_dir(str(tmp_path)):
        tasks_file = tmp_path / "tasks.toml"
        todos = Todos({}, str(tasks_file), ["Developer", "Tester"])

        task1 = Task("Task 1", "Description 1", False, "bug", "file1.py:10", "Developer")
        task2 = Task("Task 2", "Description 2", False, "feature", "file2.py:20", "Tester")
        task3 = Task("Task 3", "Description 3", False, "bug", "file3.py:30", "Developer")
        todos.add_task(task1)
        todos.add_task(task2)
        todos.add_task(task3)

        dev_tasks = todos.query_tasks_by_assignee("Developer")
        assert len(dev_tasks) == 2
        assert all(task.assignee == "Developer" for task in dev_tasks)


def test_query_tasks(tmp_path):
    with temporary_change_dir(str(tmp_path)):
        tasks_file = tmp_path / "tasks.toml"
        todos = Todos({}, str(tasks_file), ["Developer", "Tester"])

        task1 = Task("Unique Title 1", "Description", False, "bug", "file1.py:10", "Developer")
        task2 = Task("Common Title", "Description", False, "feature", "file2.py:20", "Tester")
        task3 = Task("Unique Title 2", "Description", False, "bug", "file3.py:30", "Developer")
        task4 = Task("Another Common Title", "Description", False, "bug", "file4.py:40", "Tester")
        todos.add_task(task1)
        todos.add_task(task2)
        todos.add_task(task3)
        todos.add_task(task4)

        common_title_tasks = todos.query_tasks("Common Title")
        assert len(common_title_tasks) == 2
        assert all(re.search("Common Title", task.title) for task in common_title_tasks)
