import argparse
import sys

from bug_trail.fs_utils import clear_data, prompt_and_update_gitignore
from bug_trail.views import render_all


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        int: 0 if successful, 1 if not
    """
    parser = argparse.ArgumentParser(description="Tool for local logging and error reporting.")
    parser.add_argument("--clear", action="store_true", help="Clear the database and log files")

    parser.add_argument("--output", action="store_true", help="Where to output the logs", default="logs")
    parser.add_argument("--db", action="store_true", help="Where to store the database", default="error_log.db")

    parser.add_argument("--version", action="version", version="%(prog)s 1.0")

    args = parser.parse_args()
    db_path = args.db
    log_folder = args.output
    if args.clear:
        clear_data(log_folder, db_path)
        return 0

    prompt_and_update_gitignore(".")
    # Default actions
    render_all(db_path, log_folder)
    return 0


if __name__ == "__main__":
    sys.exit(main())
