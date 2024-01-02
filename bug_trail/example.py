"""Example usage"""

# Set up logging
import logging

from bug_trail.handlers import ErrorLogSQLiteHandler

db_path = "error_log.db"
handler = ErrorLogSQLiteHandler(db_path)
logging.basicConfig(handlers=[handler], level=logging.ERROR)

# Example usage
logger = logging.getLogger(__name__)
logger.error("This is an error message")


def run():
    # Example usage
    logger2 = logging.getLogger("adhoc")
    logger2.error("This is an ad hoc error message")

    logger.error("This is an error message")
    try:
        _ = 1 / 0
    except ZeroDivisionError as e:
        logger.exception(e)


run()
