"""
Dedupe some logging code
"""
import functools
import os
from collections.abc import Callable
from typing import Any, Optional

import ai_shell.openai_schemas as schemas


def configure_logging() -> dict[str, Any]:
    """Basic style"""
    logging_config: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {"format": "[%(levelname)s] %(name)s: %(message)s"},
        },
        "handlers": {
            "default": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
            # "json": {
            #     # "()": "json_file_handler_factory",
            #     "level": "DEBUG",
            #     "class": "ai_shell.utils.json_log_handler.JSONFileHandler",
            #     "directory": "api_logs",
            #     "module_name": "openai",
            # },
        },
        "loggers": {
            # root logger can capture too much
            "": {  # root logger
                "handlers": ["default"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    debug_level_modules: list[str] = ["__main__", "ai_shell", "minimal_example"]

    info_level_modules: list[str] = []
    warn_level_modules: list[str] = []

    # json handler
    for name in ["openai"]:
        logging_config["loggers"][name] = {
            "handlers": [],  # ["json"],
            "level": "DEBUG",
            "propagate": False,
        }

    for name in debug_level_modules:
        logging_config["loggers"][name] = {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": False,
        }

    for name in info_level_modules:
        logging_config["loggers"][name] = {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        }

    for name in warn_level_modules:
        logging_config["loggers"][name] = {
            "handlers": ["default"],
            "level": "WARNING",
            "propagate": False,
        }
    return logging_config


# Determine the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Default log folder set relative to the current file
LOG_FOLDER = os.path.join(current_dir, "../logs")
# Global settings for logging
LOGGING_ENABLED = True
SESSION_LOG_FILE: Optional[str] = None


def set_log_folder(relative_path: str) -> None:
    """Set the log folder to a custom path"""
    # pylint: disable=global-statement
    global LOG_FOLDER
    LOG_FOLDER = os.path.join(current_dir, relative_path)


def log_to_executable(args: Any, kwargs: Any, func: Callable) -> None:
    """Log the command to an executable file"""
    # pylint: disable=global-statement
    global SESSION_LOG_FILE
    if LOGGING_ENABLED:
        # Ensure log folder exists
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)

        if not SESSION_LOG_FILE:
            # Number the log files
            log_files = [f for f in os.listdir(LOG_FOLDER) if f.endswith(".sh")]
            log_number = len(log_files) + 1
            log_filename = f"log_{log_number}.sh"
            mode = "w"
            SESSION_LOG_FILE = log_filename
        else:
            log_filename = SESSION_LOG_FILE
            mode = "a"

        command, subcommand = method_to_command_subcommand(func.__name__)

        # Write log to file
        with open(os.path.join(LOG_FOLDER, log_filename), mode, encoding="utf-8") as file:
            file.write(f"ais {command} {subcommand}")
            for arg in args:
                if arg is None:
                    pass
                elif str(arg).startswith("<ai_shell."):
                    # skip self,
                    pass
                elif isinstance(arg, str) and arg:
                    file.write(f' "{arg}"')
                else:
                    file.write(f" {arg}")
            for name, kwarg in kwargs.items():
                if isinstance(kwarg, bool) and kwarg:
                    file.write(f" --{name}")
                elif isinstance(kwarg, bool) and not kwarg:
                    pass
                else:
                    file.write(f' --{name}="{kwarg}"')
            file.write("\n")


def log_success_failure(result: Any, exception: Optional[Exception]) -> None:
    """Log the command to an executable file"""
    # pylint: disable=global-statement
    global SESSION_LOG_FILE
    if LOGGING_ENABLED:
        # Ensure log folder exists
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)

        if not SESSION_LOG_FILE:
            # Number the log files
            log_files = [f for f in os.listdir(LOG_FOLDER) if f.endswith(".sh")]
            log_number = len(log_files) + 1
            log_filename = f"log_{log_number}.sh"
            mode = "w"
            SESSION_LOG_FILE = log_filename
        else:
            log_filename = SESSION_LOG_FILE
            mode = "a"

        # Write log to file
        with open(os.path.join(LOG_FOLDER, log_filename), mode, encoding="utf-8") as file:
            if not exception:
                file.write(f'# Success. Return Value: "{str(result)[:40]}"\n')
            else:
                file.write(f"# Failure. Exception: {exception}\n")


def enable_logging(flag: bool) -> None:
    """Enable logging to executable file"""
    # pylint: disable=global-statement
    global LOGGING_ENABLED
    LOGGING_ENABLED = flag


def method_to_command_subcommand(method_name: str) -> tuple[str, str]:
    """Convert a method name to a command and subcommand"""
    schema = schemas._SCHEMAS
    for ns, tools in schema.items():
        for name, _ in tools.items():
            if name == method_name:
                return ns, name
    return "", ""


def log():
    """Decorator for logging commands to executable file"""

    def decorator_log(func):
        """Decorator for logging commands to executable file"""

        @functools.wraps(func)
        def wrapper_log(*args, **kwargs):
            """Decorator for logging commands to executable file"""
            # Extract for unit testing
            log_to_executable(args, kwargs, func)

            # Call the actual function
            try:
                result = func(*args, **kwargs)
                log_success_failure(result, None)
                return result
            except Exception as exception:
                log_success_failure(None, exception)
                raise

        return wrapper_log

    return decorator_log


if __name__ == "__main__":

    @log()
    def example(path: Optional[str] = ".", _some: bool = False, _long: bool = False) -> str:
        """Example"""
        # Function implementation goes here
        return f"Listing markdown files at {path}"

    # Set log folder and enable logging
    set_log_folder("custom_logs")
    enable_logging(True)
    example("~/Documents", _some=True, _long=True)
