"""
This module contains the functions for rendering the HTML templates
"""
import os

from jinja2 import Environment, FileSystemLoader

from bug_trail.data_code import fetch_log_data, fetch_log_data_grouped
from bug_trail.fs_utils import empty_folder, get_containing_folder_path


def pretty_column_name(column_name: str) -> str:
    """
    Transform a column name into a pretty name for display
    Args:
        column_name (str): The column name to be transformed
    Returns:
        str: The transformed column name
    """
    # Dictionary for special cases
    special_cases = {
        "lineno": "Line Number",
        "funcName": "Function Name",
        "exc_info": "Exception Info",
        # Add more special cases here
    }

    # Check if the column name is a special case
    if column_name in special_cases:
        return special_cases[column_name]

    # Rule-based transformation: snake_case to Title Case
    pretty_name = column_name.replace("_", " ").title()
    return pretty_name


def detail_file_name(selected_log: dict[str, str]) -> str:
    """
    Generate a filename for the detail page of a log entry

    Args:
        selected_log (dict[str, str]): The selected log entry
    Returns:
        str: The filename for the detail page
    """
    key = (
        f"{selected_log['created'].replace('.','_')}_"
        f"{selected_log['filename'].replace('.','_')}_"
        f"{selected_log['lineno']}"
    )
    return f"detail_{key}.html"


def detail_file_name_grouped(selected_log: dict[str, dict[str, str]]) -> str:
    """
    Generate a filename for the detail page of a log entry with grouped data

    Args:
        selected_log (dict[str, str]): The selected log entry
    Returns:
        str: The filename for the detail page
    """
    key = (
        f"{selected_log['TemporalDetails']['created'].replace('.','_')}_"
        f"{selected_log['SourceContext']['filename'].replace('.','_')}_"
        f"{selected_log['SourceContext']['lineno']}"
    )
    return f"detail_{key}.html"


def render_main(db_path: str, log_folder: str) -> None:
    """
    Render the main page of the log viewer

    Args:
        db_path (str): Path to the SQLite database
        log_folder (str): Path to the folder containing the log files
    """
    # Set up Jinja2 environment

    current = get_containing_folder_path(__file__)
    env = Environment(loader=FileSystemLoader(current))
    env.filters["pretty"] = pretty_column_name
    template = env.get_template("log_overview.html")

    log_data = fetch_log_data(db_path)

    for log_entry in log_data:
        log_entry["detailed_filename"] = detail_file_name(log_entry)

    # Render the template with log data
    html_output = template.render(logs=log_data)

    index = f"{log_folder}/index.html"
    os.makedirs(index.rsplit("/", 1)[0], exist_ok=True)
    with open(index, "w", encoding="utf-8") as f:
        f.write(html_output)


def render_detail(db_path: str, log_folder: str) -> None:
    """
    Render the detail page of a log entry

    Args:
        db_path (str): Path to the SQLite database
        log_folder (str): Path to the folder containing the log files
    """
    # Set up Jinja2 environment

    current = get_containing_folder_path(__file__)
    env = Environment(loader=FileSystemLoader(current))
    env.filters["pretty"] = pretty_column_name
    log_data = fetch_log_data_grouped(db_path)  # Your log records here

    # Render the template with the selected log data
    template = env.get_template("log_detail.html")

    for log_entry in log_data:
        # Selected log record for display
        selected_log = log_entry
        html_output = template.render(log=selected_log)

        # Using a unique key for each log entry, like a timestamp or a combination of fields
        key = detail_file_name_grouped(selected_log)

        # Write `html_output` to a file
        location = f"{log_folder}/{key}"
        os.makedirs(location.rsplit("/", 1)[0], exist_ok=True)
        with open(location, "w", encoding="utf-8") as f:
            f.write(html_output)


def render_all(db_path: str, logs_folder: str) -> None:
    """
    Render all the pages

    Args:
        db_path (str): Path to the SQLite database
        logs_folder (str): Path to the folder containing the log files
    """
    empty_folder(logs_folder)
    render_main(db_path, logs_folder)
    render_detail(db_path, logs_folder)


if __name__ == "__main__":
    render_all(db_path="error_log.db", logs_folder="logs")
