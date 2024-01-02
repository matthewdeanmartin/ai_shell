import datetime
import sqlite3
from typing import Any


def serialize_to_sqlite_supported(value: str) -> Any:
    """
    sqlite supports None, int, float, str, bytes by default, and also knows how to adapt datetime.date and datetime.datetime
    everything else is str(value)
    """
    if value is None:
        return value
    if isinstance(value, (int, float, str, bytes)):
        return value
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value
    return str(value)


def fetch_log_data(db_path: str) -> list[dict[str, Any]]:
    """
    Fetch all log records from the database.

    Args:
        db_path (str): Path to the SQLite database

    Returns:
        list[dict[str, Any]]: A list of dictionaries containing all log records
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to fetch all rows from the logs table
    query = "SELECT * FROM logs"
    cursor.execute(query)

    # Fetching column names from the cursor
    columns = [description[0] for description in cursor.description]

    # Fetch all rows, and convert each row to a dictionary
    rows = cursor.fetchall()
    log_data = []
    for row in rows:
        log_record = dict(zip(columns, row, strict=True))
        log_data.append(log_record)

    # Close the connection
    conn.close()
    return log_data


def fetch_log_data_grouped(db_path: str) -> Any:
    """
    Fetch all log records from the database, and group them into a nested dictionary.

    Args:
        db_path (str): Path to the SQLite database

    Returns:
        Any: A nested dictionary containing all log records
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to fetch all rows from the logs table
    query = "SELECT * FROM logs"
    cursor.execute(query)

    # Fetching column names from the cursor
    columns = [description[0] for description in cursor.description]

    # Fetch all rows, and convert each row to a grouped dictionary
    rows = cursor.fetchall()
    log_data = []
    for row in rows:
        log_record = dict(zip(columns, row, strict=True))

        # Grouping the log record
        grouped_record = {
            "MessageDetails": {key: log_record[key] for key in ["msg", "args", "levelname", "levelno"]},
            "SourceContext": {
                key: log_record[key] for key in ["name", "pathname", "filename", "module", "funcName", "lineno"]
            },
            "TemporalDetails": {key: log_record[key] for key in ["created", "msecs", "relativeCreated"]},
            "ProcessThreadContext": {
                key: log_record[key] for key in ["process", "processName", "thread", "threadName"]
            },
            "ExceptionDetails": {key: log_record[key] for key in ["exc_info", "exc_text"]},
            "StackDetails": {key: log_record[key] for key in ["stack_info"]},
            "UserData": {
                key: log_record[key]
                for key in log_record.keys()
                - {
                    "msg",
                    "args",
                    "levelname",
                    "levelno",
                    "name",
                    "pathname",
                    "filename",
                    "module",
                    "funcName",
                    "lineno",
                    "created",
                    "msecs",
                    "relativeCreated",
                    "process",
                    "processName",
                    "thread",
                    "threadName",
                    "exc_info",
                    "exc_text",
                    "stack_info",
                }
            },
        }
        log_data.append(grouped_record)

    # Close the connection
    conn.close()
    return log_data
