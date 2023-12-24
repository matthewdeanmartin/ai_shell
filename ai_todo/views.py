from collections import defaultdict
from os.path import dirname, join

from jinja2 import Environment, FileSystemLoader

from ai_todo.models import Task


def assigned_incomplete_tasks_to_markdown(assignee_name: str, tasks: list[Task]):
    # Group tasks by category
    tasks_by_category = defaultdict(list)
    for task in tasks:
        if task.assignee == assignee_name and not task.done_status:
            tasks_by_category[task.category].append(task)

    # Load template
    template_dir = join(dirname(__file__), "templates")  # Adjust path as necessary
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("task_report_template.md.j2")

    # Render template
    return template.render(
        assignee_name=assignee_name,
        tasks_by_category=tasks_by_category,
        total_tasks=sum(len(tasks) for tasks in tasks_by_category.values()),
    )


def search_results_to_markdown(search_keyword, tasks):
    # Filter tasks based on the search keyword
    matching_tasks = [task for task in tasks if search_keyword in task.title or search_keyword in task.description]

    # Load template
    template_dir = join(dirname(__file__), "templates")  # Adjust path as necessary
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("search_results_template.md.j2")

    # Render template
    return template.render(tasks=matching_tasks, total_tasks=len(matching_tasks))
