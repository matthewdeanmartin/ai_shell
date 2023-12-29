"""
AI Optimized TODO tool. Alternative to JIRA or the like.

The bot doesn't understand the assignee field.
"""
import logging
from typing import Optional

import ai_todo
from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log

logger = logging.getLogger(__name__)


class TodoTool:
    """Keep track of tasks."""

    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the TodoTool with a root folder.

        Args:
            root_folder (str): The root folder for valid files.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder: str = root_folder
        self.config = config
        self.roles = config.get_list("todo_roles")
        self.task_manager = ai_todo.TaskManager(self.root_folder, self.roles)

    @log()
    def add_todo(
        self, title: str, description: str, category: str, source_code_ref: str, assignee: Optional[str] = None
    ) -> str:
        """
        Adds a new task to the task manager.

        Args:
            title (str): The title of the task.
            description (str): A description of the task.
            category (str): The category of the task (e.g., 'bug', 'feature').
            source_code_ref (str): Reference to the source code related to the task.
            assignee (str, optional): The name of the assignee. Defaults to None.

        Returns:
            str: A confirmation message indicating successful addition of the task.
        """
        self.task_manager.add_task(title, description, category, source_code_ref, assignee)
        return "Successful"

    @log()
    def remove_todo(self, title: str) -> str:
        """
        Marks a task as finished based on its title.

        Args:
            title (str): The title of the task to be marked as finished.

        Returns:
            str: A confirmation message indicating the task was successfully marked as finished.
        """
        self.task_manager.finish_task(title)
        return "Successful"

    @log()
    def query_todos_by_regex(self, regex_pattern: str = r"[\s\S]+") -> str:
        r"""
        Queries tasks by a keyword in their title, using a regular expression pattern.

        Args:
            regex_pattern (str, optional): The regular expression pattern to match in task titles.
                                           Defaults to "[\s\S]+", which matches any title.

        Returns:
            str: The rendered Markdown string of tasks matching the given pattern.
        """
        return self.task_manager.query_by_title_keyword(regex_pattern)

    @log()
    def query_todos_by_assignee(self) -> str:
        """
        Queries tasks assigned to a specific assignee. Currently, the assignee is hard-coded as 'Developer'.

        Returns:
        str: The rendered Markdown string of tasks assigned to the specified assignee.
        """
        assignee_name = "Developer"
        return self.task_manager.query_by_assignee(assignee_name)


if __name__ == "__main__":
    tool = TodoTool(".", Config(".."))
