from ai_todo.models import Task
from ai_todo.views import assigned_incomplete_tasks_to_markdown, search_results_to_markdown


def test_assigned_incomplete_tasks_to_markdown(snapshot):
    tasks = [
        Task("Task 1", "Description 1", False, "bug", "file1.py", "Developer"),
        Task("Task 2", "Description 2", True, "feature", "file2.py", "Developer"),
        Task("Task 3", "Description 3", False, "bug", "file3.py", "Tester"),
    ]

    markdown_output = assigned_incomplete_tasks_to_markdown("Developer", tasks)
    snapshot.assert_match(markdown_output, "assigned_incomplete_tasks.mdx")


def test_search_results_to_markdown(snapshot):
    tasks = [
        Task("Bug Fix", "Fixing a critical bug", False, "bug", "bugfix.py", "Developer"),
        Task("Feature Development", "Developing a new feature", False, "feature", "feature.py", "Developer"),
        Task("Documentation", "Writing docs", False, "docs", "docs.md", "Writer"),
    ]

    markdown_output = search_results_to_markdown("Feature", tasks)
    snapshot.assert_match(markdown_output, "search_results.mdx")
