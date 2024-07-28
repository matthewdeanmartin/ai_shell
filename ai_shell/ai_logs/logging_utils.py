"""
Code-as-config for logging.
"""

import os
from typing import Any

import bug_trail_core

config_location = "pyproject.toml"
if not os.path.exists(config_location):
    config_location = "../pyproject.toml"
if not os.path.exists(config_location):
    config_location = "../../pyproject.toml"


bug_trail_config = bug_trail_core.read_config(config_path=config_location)


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
            # "bug_trail": {
            #     "level": "DEBUG",
            #     # "formatter": "standard",
            #     "class": "bug_trail_core.BugTrailHandler",
            #     "db_path": bug_trail_config.database_path,
            #     "minimum_level": logging.DEBUG,
            # },
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
                "handlers": ["default",
                             # "bug_trail"
                             ],
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
            "handlers": [
                "default",
                # "bug_trail"
            ],
            "level": "DEBUG",
            "propagate": False,
        }

    for name in info_level_modules:
        logging_config["loggers"][name] = {
            "handlers": [
                "default",
                # "bug_trail"
            ],
            "level": "INFO",
            "propagate": False,
        }

    for name in warn_level_modules:
        logging_config["loggers"][name] = {
            "handlers": [
                "default",
                # "bug_trail"
            ],
            "level": "WARNING",
            "propagate": False,
        }
    return logging_config
