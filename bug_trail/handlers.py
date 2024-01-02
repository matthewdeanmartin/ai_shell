"""
This module contains custom logging handlers.
"""

import logging
import sqlite3
import traceback

from bug_trail.data_code import serialize_to_sqlite_supported


class ErrorLogSQLiteHandler(logging.Handler):
    """
    A custom logging handler that logs to a SQLite database.
    """

    def __init__(self, db_path: str) -> None:
        """
        Initialize the handler
        Args:
            db_path (str): Path to the SQLite database
        """
        super().__init__()
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self) -> None:
        """
        Create the logs table if it doesn't exist
        """
        # Create a dummy LogRecord to introspect its attributes
        dummy_record = logging.LogRecord(
            name="", level=logging.ERROR, pathname="", lineno=0, msg="", args=(), exc_info=None
        )
        fields = [
            attr
            for attr in dir(dummy_record)
            if not callable(getattr(dummy_record, attr)) and not attr.startswith("__")
        ]
        columns = ", ".join([f"{field} TEXT" for field in fields])
        columns = columns + ", traceback TEXT"
        create_table_sql = f"CREATE TABLE IF NOT EXISTS logs ({columns})"
        self.conn.execute(create_table_sql)
        self.conn.commit()

    def emit(self, record: logging.LogRecord) -> None:
        """
        Insert a log record into the database

        Args:
            record (logging.LogRecord): The log record to be inserted
        """
        if record.levelno < logging.ERROR:
            return
        # Check if there is exception information
        if record.exc_info:
            # Format the traceback
            traceback_str = "".join(traceback.format_exception(*record.exc_info))
            record.traceback = traceback_str
        else:
            record.traceback = None

        insert_sql = "INSERT INTO logs ({fields}) VALUES ({values})"
        field_names = ", ".join(
            [attr for attr in dir(record) if not attr.startswith("__") and not attr == "getMessage"]
        )
        field_names = field_names + ", traceback"
        field_values = ", ".join(["?" for _ in field_names.split(", ")])
        formatted_sql = insert_sql.format(fields=field_names, values=field_values)
        args = [getattr(record, field, "") for field in field_names.split(", ")]
        args = [serialize_to_sqlite_supported(arg) for arg in args]
        self.conn.execute(formatted_sql, args)
        self.conn.commit()

    def close(self) -> None:
        """
        Close the connection to the database
        """
        if self.conn:
            self.conn.close()
        super().close()
