"""
Generated code, do not edit.
"""
import argparse

from ai_shell.answer_tool import AnswerCollectorTool
from ai_shell.cat_tool import CatTool
from ai_shell.cut_tool import CutTool
from ai_shell.find_tool import FindTool
from ai_shell.git_tool import GitTool
from ai_shell.grep_tool import GrepTool
from ai_shell.head_tail_tool import HeadTailTool
from ai_shell.insert_tool import InsertTool
from ai_shell.ls_tool import LsTool
from ai_shell.patch_tool import PatchTool
from ai_shell.pytest_tool import PytestTool
from ai_shell.replace_tool import ReplaceTool
from ai_shell.rewrite_tool import RewriteTool
from ai_shell.todo_tool import TodoTool
from ai_shell.token_tool import TokenCounterTool
from ai_shell.utils.config_manager import Config
from ai_shell.utils.console_utils import pretty_console

# pylint: disable=unused-argument


CONFIG = Config()


def head_command(args):
    """Invoke head"""
    tool = HeadTailTool(".", CONFIG)
    pretty_console(
        tool.head(
            byte_count=args.byte_count,
            file_path=args.file_path,
            lines=args.lines,
        )
    )


def head_markdown_command(args):
    """Invoke head_markdown"""
    tool = HeadTailTool(".", CONFIG)
    pretty_console(
        tool.head_markdown(
            file_path=args.file_path,
            lines=args.lines,
        )
    )


def head_tail_command(args):
    """Invoke head_tail"""
    tool = HeadTailTool(".", CONFIG)
    pretty_console(
        tool.head_tail(
            byte_count=args.byte_count,
            file_path=args.file_path,
            lines=args.lines,
            mode=args.mode,
        )
    )


def tail_command(args):
    """Invoke tail"""
    tool = HeadTailTool(".", CONFIG)
    pretty_console(
        tool.tail(
            byte_count=args.byte_count,
            file_path=args.file_path,
            lines=args.lines,
        )
    )


def tail_markdown_command(args):
    """Invoke tail_markdown"""
    tool = HeadTailTool(".", CONFIG)
    pretty_console(
        tool.tail_markdown(
            file_path=args.file_path,
            lines=args.lines,
        )
    )


def cat_command(args):
    """Invoke cat"""
    tool = CatTool(".", CONFIG)
    pretty_console(
        tool.cat(
            file_paths=args.file_paths,
            number_lines=args.number_lines,
            squeeze_blank=args.squeeze_blank,
        )
    )


def cat_markdown_command(args):
    """Invoke cat_markdown"""
    tool = CatTool(".", CONFIG)
    pretty_console(
        tool.cat_markdown(
            file_paths=args.file_paths,
            number_lines=args.number_lines,
            squeeze_blank=args.squeeze_blank,
        )
    )


def cut_characters_command(args):
    """Invoke cut_characters"""
    tool = CutTool(".", CONFIG)
    pretty_console(
        tool.cut_characters(
            character_ranges=args.character_ranges,
            file_path=args.file_path,
        )
    )


def cut_fields_command(args):
    """Invoke cut_fields"""
    tool = CutTool(".", CONFIG)
    pretty_console(
        tool.cut_fields(
            delimiter=args.delimiter,
            field_ranges=args.field_ranges,
            filename=args.filename,
        )
    )


def cut_fields_by_name_command(args):
    """Invoke cut_fields_by_name"""
    tool = CutTool(".", CONFIG)
    pretty_console(
        tool.cut_fields_by_name(
            delimiter=args.delimiter,
            field_names=args.field_names,
            filename=args.filename,
        )
    )


def find_files_command(args):
    """Invoke find_files"""
    tool = FindTool(".", CONFIG)
    pretty_console(
        tool.find_files(
            file_type=args.file_type,
            name=args.name,
            regex=args.regex,
            size=args.size,
        )
    )


def find_files_markdown_command(args):
    """Invoke find_files_markdown"""
    tool = FindTool(".", CONFIG)
    pretty_console(
        tool.find_files_markdown(
            file_type=args.file_type,
            name=args.name,
            regex=args.regex,
            size=args.size,
        )
    )


def get_current_branch_command(args):
    """Invoke get_current_branch"""
    tool = GitTool(".", CONFIG)
    pretty_console(tool.get_current_branch())


def get_recent_commits_command(args):
    """Invoke get_recent_commits"""
    tool = GitTool(".", CONFIG)
    pretty_console(
        tool.get_recent_commits(
            n=args.n,
            short_hash=args.short_hash,
        )
    )


def git_diff_command(args):
    """Invoke git_diff"""
    tool = GitTool(".", CONFIG)
    pretty_console(tool.git_diff())


def git_diff_commit_command(args):
    """Invoke git_diff_commit"""
    tool = GitTool(".", CONFIG)
    pretty_console(
        tool.git_diff_commit(
            commit1=args.commit1,
            commit2=args.commit2,
        )
    )


def git_log_file_command(args):
    """Invoke git_log_file"""
    tool = GitTool(".", CONFIG)
    pretty_console(
        tool.git_log_file(
            filename=args.filename,
        )
    )


def git_log_search_command(args):
    """Invoke git_log_search"""
    tool = GitTool(".", CONFIG)
    pretty_console(
        tool.git_log_search(
            search_string=args.search_string,
        )
    )


def git_show_command(args):
    """Invoke git_show"""
    tool = GitTool(".", CONFIG)
    pretty_console(tool.git_show())


def git_status_command(args):
    """Invoke git_status"""
    tool = GitTool(".", CONFIG)
    pretty_console(tool.git_status())


def is_ignored_by_gitignore_command(args):
    """Invoke is_ignored_by_gitignore"""
    tool = GitTool(".", CONFIG)
    pretty_console(
        tool.is_ignored_by_gitignore(
            file_path=args.file_path,
            gitignore_path=args.gitignore_path,
        )
    )


def apply_git_patch_command(args):
    """Invoke apply_git_patch"""
    tool = PatchTool(".", CONFIG)
    pretty_console(
        tool.apply_git_patch(
            patch_content=args.patch_content,
        )
    )


def ls_command(args):
    """Invoke ls"""
    tool = LsTool(".", CONFIG)
    pretty_console(
        tool.ls(
            all_files=args.all_files,
            long=args.long,
            path=args.path,
        )
    )


def ls_markdown_command(args):
    """Invoke ls_markdown"""
    tool = LsTool(".", CONFIG)
    pretty_console(
        tool.ls_markdown(
            all_files=args.all_files,
            long=args.long,
            path=args.path,
        )
    )


def grep_command(args):
    """Invoke grep"""
    tool = GrepTool(".", CONFIG)
    pretty_console(
        tool.grep(
            glob_pattern=args.glob_pattern,
            maximum_matches_per_file=args.maximum_matches_per_file,
            maximum_matches_total=args.maximum_matches_total,
            regex=args.regex,
            skip_first_matches=args.skip_first_matches,
        )
    )


def grep_markdown_command(args):
    """Invoke grep_markdown"""
    tool = GrepTool(".", CONFIG)
    pretty_console(
        tool.grep_markdown(
            glob_pattern=args.glob_pattern,
            maximum_matches=args.maximum_matches,
            regex=args.regex,
            skip_first_matches=args.skip_first_matches,
        )
    )


def count_tokens_command(args):
    """Invoke count_tokens"""
    tool = TokenCounterTool(".", CONFIG)
    pretty_console(
        tool.count_tokens(
            text=args.text,
        )
    )


def add_todo_command(args):
    """Invoke add_todo"""
    tool = TodoTool(".", CONFIG)
    pretty_console(
        tool.add_todo(
            assignee=args.assignee,
            category=args.category,
            description=args.description,
            source_code_ref=args.source_code_ref,
            title=args.title,
        )
    )


def query_todos_by_assignee_command(args):
    """Invoke query_todos_by_assignee"""
    tool = TodoTool(".", CONFIG)
    pretty_console(tool.query_todos_by_assignee())


def query_todos_by_regex_command(args):
    """Invoke query_todos_by_regex"""
    tool = TodoTool(".", CONFIG)
    pretty_console(
        tool.query_todos_by_regex(
            regex_pattern=args.regex_pattern,
        )
    )


def remove_todo_command(args):
    """Invoke remove_todo"""
    tool = TodoTool(".", CONFIG)
    pretty_console(
        tool.remove_todo(
            title=args.title,
        )
    )


def insert_text_after_context_command(args):
    """Invoke insert_text_after_context"""
    tool = InsertTool(".", CONFIG)
    pretty_console(
        tool.insert_text_after_context(
            context=args.context,
            file_path=args.file_path,
            text_to_insert=args.text_to_insert,
        )
    )


def insert_text_after_multiline_context_command(args):
    """Invoke insert_text_after_multiline_context"""
    tool = InsertTool(".", CONFIG)
    pretty_console(
        tool.insert_text_after_multiline_context(
            context_lines=args.context_lines,
            file_path=args.file_path,
            text_to_insert=args.text_to_insert,
        )
    )


def insert_text_at_start_or_end_command(args):
    """Invoke insert_text_at_start_or_end"""
    tool = InsertTool(".", CONFIG)
    pretty_console(
        tool.insert_text_at_start_or_end(
            file_path=args.file_path,
            position=args.position,
            text_to_insert=args.text_to_insert,
        )
    )


def replace_all_command(args):
    """Invoke replace_all"""
    tool = ReplaceTool(".", CONFIG)
    pretty_console(
        tool.replace_all(
            file_path=args.file_path,
            new_text=args.new_text,
            old_text=args.old_text,
        )
    )


def replace_line_by_line_command(args):
    """Invoke replace_line_by_line"""
    tool = ReplaceTool(".", CONFIG)
    pretty_console(
        tool.replace_line_by_line(
            file_path=args.file_path,
            line_end=args.line_end,
            line_start=args.line_start,
            new_text=args.new_text,
            old_text=args.old_text,
        )
    )


def replace_with_regex_command(args):
    """Invoke replace_with_regex"""
    tool = ReplaceTool(".", CONFIG)
    pretty_console(
        tool.replace_with_regex(
            file_path=args.file_path,
            regex_match_expression=args.regex_match_expression,
            replacement=args.replacement,
        )
    )


def save_if_changed_command(args):
    """Invoke save_if_changed"""
    tool = ReplaceTool(".", CONFIG)
    pretty_console(
        tool.save_if_changed(
            file_path=args.file_path,
            final=args.final,
            input_text=args.input_text,
        )
    )


def revert_to_latest_backup_command(args):
    """Invoke revert_to_latest_backup"""
    tool = RewriteTool(".", CONFIG)
    pretty_console(
        tool.revert_to_latest_backup(
            file_name=args.file_name,
        )
    )


def rewrite_file_command(args):
    """Invoke rewrite_file"""
    tool = RewriteTool(".", CONFIG)
    pretty_console(
        tool.rewrite_file(
            file_path=args.file_path,
            text=args.text,
        )
    )


def write_new_file_command(args):
    """Invoke write_new_file"""
    tool = RewriteTool(".", CONFIG)
    pretty_console(
        tool.write_new_file(
            file_path=args.file_path,
            text=args.text,
        )
    )


def report_bool_command(args):
    """Invoke report_bool"""
    tool = AnswerCollectorTool(".", CONFIG)
    pretty_console(
        tool.report_bool(
            answer=args.answer,
            comment=args.comment,
        )
    )


def report_dict_command(args):
    """Invoke report_dict"""
    tool = AnswerCollectorTool(".", CONFIG)
    pretty_console(
        tool.report_dict(
            answer=args.answer,
            comment=args.comment,
        )
    )


def report_float_command(args):
    """Invoke report_float"""
    tool = AnswerCollectorTool(".", CONFIG)
    pretty_console(
        tool.report_float(
            answer=args.answer,
            comment=args.comment,
        )
    )


def report_int_command(args):
    """Invoke report_int"""
    tool = AnswerCollectorTool(".", CONFIG)
    pretty_console(
        tool.report_int(
            answer=args.answer,
            comment=args.comment,
        )
    )


def report_json_command(args):
    """Invoke report_json"""
    tool = AnswerCollectorTool(".", CONFIG)
    pretty_console(
        tool.report_json(
            answer=args.answer,
            comment=args.comment,
        )
    )


def report_list_command(args):
    """Invoke report_list"""
    tool = AnswerCollectorTool(".", CONFIG)
    pretty_console(
        tool.report_list(
            answer=args.answer,
            comment=args.comment,
        )
    )


def report_set_command(args):
    """Invoke report_set"""
    tool = AnswerCollectorTool(".", CONFIG)
    pretty_console(
        tool.report_set(
            answer=args.answer,
            comment=args.comment,
        )
    )


def report_text_command(args):
    """Invoke report_text"""
    tool = AnswerCollectorTool(".", CONFIG)
    pretty_console(
        tool.report_text(
            answer=args.answer,
            comment=args.comment,
        )
    )


def report_toml_command(args):
    """Invoke report_toml"""
    tool = AnswerCollectorTool(".", CONFIG)
    pretty_console(
        tool.report_toml(
            answer=args.answer,
            comment=args.comment,
        )
    )


def report_tuple_command(args):
    """Invoke report_tuple"""
    tool = AnswerCollectorTool(".", CONFIG)
    pretty_console(
        tool.report_tuple(
            answer=args.answer,
            comment=args.comment,
        )
    )


def report_xml_command(args):
    """Invoke report_xml"""
    tool = AnswerCollectorTool(".", CONFIG)
    pretty_console(
        tool.report_xml(
            answer=args.answer,
            comment=args.comment,
        )
    )


def pytest_command(args):
    """Invoke pytest"""
    tool = PytestTool(".", CONFIG)
    pretty_console(tool.pytest())


def run():
    """Create the main parser"""
    parser = argparse.ArgumentParser(prog="ais", description="AI Shell Command Line Interface")
    subparsers = parser.add_subparsers(dest="subcommand", help="sub-command help")
    # Create a parser for the "head" command
    head_parser = subparsers.add_parser("head", help="""Return the first \'lines\' or \'byte_count\' from a file..""")

    head_parser.add_argument(
        "--byte-count", dest="byte_count", help="""Number of bytes to return. If specified, overrides lines."""
    )

    head_parser.add_argument("--file-path", dest="file_path", help="""Path to the file.""")

    head_parser.add_argument(
        "--lines",
        dest="lines",
        help="""Number of lines to return. Ignored if byte_count is specified. Defaults to 10.""",
    )

    head_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    head_parser.set_defaults(func=head_command)

    # Create a parser for the "head_markdown" command
    head_markdown_parser = subparsers.add_parser(
        "head_markdown", help="""Return the first \'lines\' lines of a file formatted as markdown.."""
    )

    head_markdown_parser.add_argument("--file-path", dest="file_path", help="""Path to the file.""")

    head_markdown_parser.add_argument("--lines", dest="lines", help="""Number of lines to return. Defaults to 10.""")

    head_markdown_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    head_markdown_parser.set_defaults(func=head_markdown_command)

    # Create a parser for the "head_tail" command
    head_tail_parser = subparsers.add_parser(
        "head_tail", help="""Read lines or bytes from the start (\'head\') or end (\'tail\') of a file.."""
    )

    head_tail_parser.add_argument(
        "--byte-count", dest="byte_count", help="""Number of bytes to read. If specified, overrides lines."""
    )

    head_tail_parser.add_argument("--file-path", dest="file_path", help="""Path to the file.""")

    head_tail_parser.add_argument(
        "--lines", dest="lines", help="""Number of lines to read. Ignored if byte_count is specified. Defaults to 10."""
    )

    head_tail_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    head_tail_parser.add_argument(
        "--mode", dest="mode", help="""Operation mode, either \'head\' or \'tail\'. Defaults to \'head\'."""
    )
    head_tail_parser.set_defaults(func=head_tail_command)

    # Create a parser for the "tail" command
    tail_parser = subparsers.add_parser("tail", help="""Return the last \'lines\' or \'bytes\' from a file..""")

    tail_parser.add_argument(
        "--byte-count", dest="byte_count", help="""Number of bytes to return. If specified, overrides lines."""
    )

    tail_parser.add_argument("--file-path", dest="file_path", help="""Path to the file.""")

    tail_parser.add_argument(
        "--lines",
        dest="lines",
        help="""Number of lines to return. Ignored if byte_count is specified. Defaults to 10.""",
    )

    tail_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    tail_parser.set_defaults(func=tail_command)

    # Create a parser for the "tail_markdown" command
    tail_markdown_parser = subparsers.add_parser(
        "tail_markdown", help="""Return the last \'lines\' lines of a file formatted as markdown.."""
    )

    tail_markdown_parser.add_argument("--file-path", dest="file_path", help="""Path to the file.""")

    tail_markdown_parser.add_argument("--lines", dest="lines", help="""Number of lines to return. Defaults to 10.""")

    tail_markdown_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    tail_markdown_parser.set_defaults(func=tail_markdown_command)

    # Create a parser for the "cat" command
    cat_parser = subparsers.add_parser(
        "cat", help="""Mimics the basic functionalities of the \'cat\' command in Unix.."""
    )

    cat_parser.add_argument("--file-paths", dest="file_paths", help="""A list of file paths to concatenate.""")

    cat_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    cat_parser.add_argument(
        "--number-lines", dest="number_lines", action="store_true", help="""If True, number all output lines."""
    )

    cat_parser.add_argument(
        "--squeeze-blank",
        dest="squeeze_blank",
        action="store_true",
        help="""If True, consecutive blank lines are squeezed to one.""",
    )
    cat_parser.set_defaults(func=cat_command)

    # Create a parser for the "cat_markdown" command
    cat_markdown_parser = subparsers.add_parser(
        "cat_markdown", help="""Concatenates the content of given file paths and formats them as markdown.."""
    )

    cat_markdown_parser.add_argument("--file-paths", dest="file_paths", help="""List of file paths to concatenate.""")

    cat_markdown_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    cat_markdown_parser.add_argument(
        "--number-lines", dest="number_lines", action="store_true", help="""If True, number all output lines."""
    )

    cat_markdown_parser.add_argument(
        "--squeeze-blank",
        dest="squeeze_blank",
        action="store_true",
        help="""If True, consecutive blank lines are squeezed to one.""",
    )
    cat_markdown_parser.set_defaults(func=cat_markdown_command)

    # Create a parser for the "cut_characters" command
    cut_characters_parser = subparsers.add_parser(
        "cut_characters", help="""Reads a file and extracts characters based on specified ranges.."""
    )

    cut_characters_parser.add_argument(
        "--character-ranges",
        dest="character_ranges",
        help="""A string representing character ranges, e.g., "1-5,10".""",
    )

    cut_characters_parser.add_argument("--file-path", dest="file_path", help="""The name of the file to process.""")

    cut_characters_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    cut_characters_parser.set_defaults(func=cut_characters_command)

    # Create a parser for the "cut_fields" command
    cut_fields_parser = subparsers.add_parser(
        "cut_fields", help="""Reads a file and extracts fields based on specified ranges using the given delimiter.."""
    )

    cut_fields_parser.add_argument(
        "--delimiter", dest="delimiter", help="""A single character used as the field delimiter."""
    )

    cut_fields_parser.add_argument(
        "--field-ranges", dest="field_ranges", help="""A string representing field ranges, e.g., "1-3,5"."""
    )

    cut_fields_parser.add_argument("--filename", dest="filename", help="""The name of the file to process.""")

    cut_fields_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    cut_fields_parser.set_defaults(func=cut_fields_command)

    # Create a parser for the "cut_fields_by_name" command
    cut_fields_by_name_parser = subparsers.add_parser(
        "cut_fields_by_name",
        help="""Reads a file and extracts fields based on specified field names using the given delimiter..""",
    )

    cut_fields_by_name_parser.add_argument(
        "--delimiter", dest="delimiter", help="""A single character used as the field delimiter."""
    )

    cut_fields_by_name_parser.add_argument(
        "--field-names", dest="field_names", help="""A list of field names to extract."""
    )

    cut_fields_by_name_parser.add_argument("--filename", dest="filename", help="""The name of the file to process.""")

    cut_fields_by_name_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    cut_fields_by_name_parser.set_defaults(func=cut_fields_by_name_command)

    # Create a parser for the "find_files" command
    find_files_parser = subparsers.add_parser(
        "find_files",
        help="""Recursively search for files or directories matching given criteria in a directory and its subdirectories..""",
    )

    find_files_parser.add_argument(
        "--file-type", dest="file_type", help="""The type to filter (\'file\' or \'directory\')."""
    )

    find_files_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    find_files_parser.add_argument("--name", dest="name", help="""The exact name to match filenames against.""")

    find_files_parser.add_argument("--regex", dest="regex", help="""The regex pattern to match filenames against.""")

    find_files_parser.add_argument(
        "--size", dest="size", help="""The size to filter files by, e.g., \'+100\' for files larger than 100 bytes."""
    )
    find_files_parser.set_defaults(func=find_files_command)

    # Create a parser for the "find_files_markdown" command
    find_files_markdown_parser = subparsers.add_parser(
        "find_files_markdown",
        help="""Recursively search for files or directories matching given criteria in a directory and its subdirectories..""",
    )

    find_files_markdown_parser.add_argument(
        "--file-type", dest="file_type", help="""The type to filter (\'file\' or \'directory\')."""
    )

    find_files_markdown_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    find_files_markdown_parser.add_argument(
        "--name", dest="name", help="""The exact name to match filenames against."""
    )

    find_files_markdown_parser.add_argument(
        "--regex", dest="regex", help="""The regex pattern to match filenames against."""
    )

    find_files_markdown_parser.add_argument(
        "--size", dest="size", help="""The size to filter files by, e.g., \'+100\' for files larger than 100 bytes."""
    )
    find_files_markdown_parser.set_defaults(func=find_files_markdown_command)

    # Create a parser for the "get_current_branch" command
    get_current_branch_parser = subparsers.add_parser(
        "get_current_branch", help="""Retrieves the current branch name of the repository.."""
    )

    get_current_branch_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    get_current_branch_parser.set_defaults(func=get_current_branch_command)

    # Create a parser for the "get_recent_commits" command
    get_recent_commits_parser = subparsers.add_parser(
        "get_recent_commits", help="""Retrieves the most recent commit hashes from the current branch.."""
    )

    get_recent_commits_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    get_recent_commits_parser.add_argument(
        "--n", dest="n", help="""The number of recent commits to retrieve. Defaults to 10."""
    )

    get_recent_commits_parser.add_argument(
        "--short-hash",
        dest="short_hash",
        action="store_true",
        help="""If True, return short hashes; otherwise, return full hashes. Defaults to False.""",
    )
    get_recent_commits_parser.set_defaults(func=get_recent_commits_command)

    # Create a parser for the "git_diff" command
    git_diff_parser = subparsers.add_parser("git_diff", help="""Returns the differences in the working directory..""")

    git_diff_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    git_diff_parser.set_defaults(func=git_diff_command)

    # Create a parser for the "git_diff_commit" command
    git_diff_commit_parser = subparsers.add_parser("git_diff_commit", help="""Shows changes between two commits..""")

    git_diff_commit_parser.add_argument("--commit1", dest="commit1", help="""First commit""")

    git_diff_commit_parser.add_argument("--commit2", dest="commit2", help="""Second commit""")

    git_diff_commit_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    git_diff_commit_parser.set_defaults(func=git_diff_commit_command)

    # Create a parser for the "git_log_file" command
    git_log_file_parser = subparsers.add_parser(
        "git_log_file", help="""Returns the commit history for a specific file.."""
    )

    git_log_file_parser.add_argument("--filename", dest="filename", help="""The path to the file.""")

    git_log_file_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    git_log_file_parser.set_defaults(func=git_log_file_command)

    # Create a parser for the "git_log_search" command
    git_log_search_parser = subparsers.add_parser(
        "git_log_search", help="""Returns the commit history that matches the search string.."""
    )

    git_log_search_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    git_log_search_parser.add_argument("--search-string", dest="search_string", help="""The search string.""")
    git_log_search_parser.set_defaults(func=git_log_search_command)

    # Create a parser for the "git_show" command
    git_show_parser = subparsers.add_parser(
        "git_show", help="""Shows various types of objects (commits, tags, etc.).."""
    )

    git_show_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    git_show_parser.set_defaults(func=git_show_command)

    # Create a parser for the "git_status" command
    git_status_parser = subparsers.add_parser("git_status", help="""Returns the status of the repository..""")

    git_status_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    git_status_parser.set_defaults(func=git_status_command)

    # Create a parser for the "is_ignored_by_gitignore" command
    is_ignored_by_gitignore_parser = subparsers.add_parser(
        "is_ignored_by_gitignore", help="""Check if a file is ignored by .gitignore.."""
    )

    is_ignored_by_gitignore_parser.add_argument(
        "--file-path", dest="file_path", help="""The path of the file to check."""
    )

    is_ignored_by_gitignore_parser.add_argument(
        "--gitignore-path",
        dest="gitignore_path",
        help="""The path to the .gitignore file. Defaults to \'.gitignore\' in the current directory.""",
    )

    is_ignored_by_gitignore_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    is_ignored_by_gitignore_parser.set_defaults(func=is_ignored_by_gitignore_command)

    # Create a parser for the "apply_git_patch" command
    apply_git_patch_parser = subparsers.add_parser(
        "apply_git_patch", help="""Apply a git patch to the files in the root folder.."""
    )

    apply_git_patch_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    apply_git_patch_parser.add_argument(
        "--patch-content", dest="patch_content", help="""The content of the git patch."""
    )
    apply_git_patch_parser.set_defaults(func=apply_git_patch_command)

    # Create a parser for the "ls" command
    ls_parser = subparsers.add_parser(
        "ls", help="""List directory contents, with options to include all files and detailed view.."""
    )

    ls_parser.add_argument(
        "--all-files",
        dest="all_files",
        action="store_true",
        help="""If True, include hidden files. Defaults to False.""",
    )

    ls_parser.add_argument(
        "--long",
        dest="long",
        action="store_true",
        help="""If True, include details like permissions, owner, size, and modification date. Defaults to False.""",
    )

    ls_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    ls_parser.add_argument(
        "--path", dest="path", help="""The directory path to list. Defaults to the current directory \'.\'."""
    )
    ls_parser.set_defaults(func=ls_command)

    # Create a parser for the "ls_markdown" command
    ls_markdown_parser = subparsers.add_parser(
        "ls_markdown", help="""List directory contents, with options to include all files and detailed view.."""
    )

    ls_markdown_parser.add_argument(
        "--all-files",
        dest="all_files",
        action="store_true",
        help="""If True, include hidden files. Defaults to False.""",
    )

    ls_markdown_parser.add_argument(
        "--long",
        dest="long",
        action="store_true",
        help="""If True, include details like permissions, owner, size, and modification date. Defaults to False.""",
    )

    ls_markdown_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    ls_markdown_parser.add_argument(
        "--path", dest="path", help="""The directory path to list. Defaults to the current directory \'.\'."""
    )
    ls_markdown_parser.set_defaults(func=ls_markdown_command)

    # Create a parser for the "grep" command
    grep_parser = subparsers.add_parser(
        "grep", help="""Search for lines matching a regular expression in files specified by a glob pattern.."""
    )

    grep_parser.add_argument("--glob-pattern", dest="glob_pattern", help="""A glob pattern string to specify files.""")

    grep_parser.add_argument(
        "--maximum-matches-per-file",
        dest="maximum_matches_per_file",
        help="""Maximum number of matches to return for one file.""",
    )

    grep_parser.add_argument(
        "--maximum-matches-total", dest="maximum_matches_total", help="""Maximum number of matches to return total."""
    )

    grep_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    grep_parser.add_argument("--regex", dest="regex", help="""A regular expression string to search for.""")

    grep_parser.add_argument(
        "--skip-first-matches", dest="skip_first_matches", help="""Number of initial matches to skip."""
    )
    grep_parser.set_defaults(func=grep_command)

    # Create a parser for the "grep_markdown" command
    grep_markdown_parser = subparsers.add_parser(
        "grep_markdown",
        help="""Search for lines matching a regular expression in files and returns markdown formatted results..""",
    )

    grep_markdown_parser.add_argument(
        "--glob-pattern", dest="glob_pattern", help="""A glob pattern string to specify files."""
    )

    grep_markdown_parser.add_argument(
        "--maximum-matches", dest="maximum_matches", help="""Maximum number of matches to return."""
    )

    grep_markdown_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    grep_markdown_parser.add_argument("--regex", dest="regex", help="""A regular expression string to search for.""")

    grep_markdown_parser.add_argument(
        "--skip-first-matches", dest="skip_first_matches", help="""Number of initial matches to skip."""
    )
    grep_markdown_parser.set_defaults(func=grep_markdown_command)

    # Create a parser for the "count_tokens" command
    count_tokens_parser = subparsers.add_parser("count_tokens", help="""Count the number of tokens in a string..""")

    count_tokens_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    count_tokens_parser.add_argument("--text", dest="text", help="""The text to count the tokens in.""")
    count_tokens_parser.set_defaults(func=count_tokens_command)

    # Create a parser for the "add_todo" command
    add_todo_parser = subparsers.add_parser("add_todo", help="""Adds a new task to the task manager..""")

    add_todo_parser.add_argument("--assignee", dest="assignee", help="""The name of the assignee. Defaults to None.""")

    add_todo_parser.add_argument(
        "--category", dest="category", help="""The category of the task (e.g., \'bug\', \'feature\')."""
    )

    add_todo_parser.add_argument("--description", dest="description", help="""A description of the task.""")

    add_todo_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    add_todo_parser.add_argument(
        "--source-code-ref", dest="source_code_ref", help="""Reference to the source code related to the task."""
    )

    add_todo_parser.add_argument("--title", dest="title", help="""The title of the task.""")
    add_todo_parser.set_defaults(func=add_todo_command)

    # Create a parser for the "query_todos_by_assignee" command
    query_todos_by_assignee_parser = subparsers.add_parser(
        "query_todos_by_assignee",
        help="""Queries tasks assigned to a specific assignee. Currently, the assignee is hard-coded as \'Developer\'..""",
    )

    query_todos_by_assignee_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    query_todos_by_assignee_parser.set_defaults(func=query_todos_by_assignee_command)

    # Create a parser for the "query_todos_by_regex" command
    query_todos_by_regex_parser = subparsers.add_parser(
        "query_todos_by_regex",
        help="""Queries tasks by a keyword in their title, using a regular expression pattern..""",
    )

    query_todos_by_regex_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    query_todos_by_regex_parser.add_argument(
        "--regex-pattern",
        dest="regex_pattern",
        help=r"""The regular expression pattern to match in task titles.
Defaults to "[\s\S]+", which matches any title.""",
    )
    query_todos_by_regex_parser.set_defaults(func=query_todos_by_regex_command)

    # Create a parser for the "remove_todo" command
    remove_todo_parser = subparsers.add_parser("remove_todo", help="""Marks a task as finished based on its title..""")

    remove_todo_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    remove_todo_parser.add_argument("--title", dest="title", help="""The title of the task to be marked as finished.""")
    remove_todo_parser.set_defaults(func=remove_todo_command)

    # Create a parser for the "insert_text_after_context" command
    insert_text_after_context_parser = subparsers.add_parser(
        "insert_text_after_context", help="""Inserts a given text immediately after a specified context in a file.."""
    )

    insert_text_after_context_parser.add_argument(
        "--context",
        dest="context",
        help="""The context string to search for in the file. The text is
inserted after the line containing this context.""",
    )

    insert_text_after_context_parser.add_argument(
        "--file-path", dest="file_path", help="""The path of the file in which the text is to be inserted."""
    )

    insert_text_after_context_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    insert_text_after_context_parser.add_argument(
        "--text-to-insert", dest="text_to_insert", help="""The text to insert into the file."""
    )
    insert_text_after_context_parser.set_defaults(func=insert_text_after_context_command)

    # Create a parser for the "insert_text_after_multiline_context" command
    insert_text_after_multiline_context_parser = subparsers.add_parser(
        "insert_text_after_multiline_context",
        help="""Inserts text immediately after a specified multiline context in a file..""",
    )

    insert_text_after_multiline_context_parser.add_argument(
        "--context-lines",
        dest="context_lines",
        help="""A list of strings representing the multiline
context to search for in the file.""",
    )

    insert_text_after_multiline_context_parser.add_argument(
        "--file-path", dest="file_path", help="""The path of the file in which the text is to be inserted."""
    )

    insert_text_after_multiline_context_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    insert_text_after_multiline_context_parser.add_argument(
        "--text-to-insert", dest="text_to_insert", help="""The text to insert into the file after the context."""
    )
    insert_text_after_multiline_context_parser.set_defaults(func=insert_text_after_multiline_context_command)

    # Create a parser for the "insert_text_at_start_or_end" command
    insert_text_at_start_or_end_parser = subparsers.add_parser(
        "insert_text_at_start_or_end", help="""Inserts text at the start or end of a file.."""
    )

    insert_text_at_start_or_end_parser.add_argument(
        "--file-path", dest="file_path", help="""The path of the file in which the text is to be inserted."""
    )

    insert_text_at_start_or_end_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    insert_text_at_start_or_end_parser.add_argument(
        "--position",
        dest="position",
        help="""The position where the text should be inserted.
Should be either \'start\' or \'end\'. Defaults to \'end\'.""",
    )

    insert_text_at_start_or_end_parser.add_argument(
        "--text-to-insert", dest="text_to_insert", help="""The text to insert into the file."""
    )
    insert_text_at_start_or_end_parser.set_defaults(func=insert_text_at_start_or_end_command)

    # Create a parser for the "replace_all" command
    replace_all_parser = subparsers.add_parser(
        "replace_all", help="""Replaces all occurrences of a specified text with new text in a file.."""
    )

    replace_all_parser.add_argument("--file-path", dest="file_path", help="""The path to the file.""")

    replace_all_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    replace_all_parser.add_argument("--new-text", dest="new_text", help="""The new text to replace the old text.""")

    replace_all_parser.add_argument("--old-text", dest="old_text", help="""The text to be replaced.""")
    replace_all_parser.set_defaults(func=replace_all_command)

    # Create a parser for the "replace_line_by_line" command
    replace_line_by_line_parser = subparsers.add_parser(
        "replace_line_by_line",
        help="""Replaces occurrences of a specified text with new text in a range of lines in a file..""",
    )

    replace_line_by_line_parser.add_argument("--file-path", dest="file_path", help="""The path to the file.""")

    replace_line_by_line_parser.add_argument(
        "--line-end",
        dest="line_end",
        help="""The ending line number (0-indexed) for the replacement.
If -1, it goes to the end of the file. Defaults to -1.""",
    )

    replace_line_by_line_parser.add_argument(
        "--line-start",
        dest="line_start",
        help="""The starting line number (0-indexed) for the replacement.
Defaults to 0.""",
    )

    replace_line_by_line_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    replace_line_by_line_parser.add_argument(
        "--new-text", dest="new_text", help="""The new text to replace the old text."""
    )

    replace_line_by_line_parser.add_argument("--old-text", dest="old_text", help="""The text to be replaced.""")
    replace_line_by_line_parser.set_defaults(func=replace_line_by_line_command)

    # Create a parser for the "replace_with_regex" command
    replace_with_regex_parser = subparsers.add_parser(
        "replace_with_regex", help="""Replaces text in a file based on a regular expression match.."""
    )

    replace_with_regex_parser.add_argument("--file-path", dest="file_path", help="""The path to the file.""")

    replace_with_regex_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    replace_with_regex_parser.add_argument(
        "--regex-match-expression", dest="regex_match_expression", help="""The regular expression pattern to match."""
    )

    replace_with_regex_parser.add_argument(
        "--replacement", dest="replacement", help="""The text to replace the matched pattern."""
    )
    replace_with_regex_parser.set_defaults(func=replace_with_regex_command)

    # Create a parser for the "save_if_changed" command
    save_if_changed_parser = subparsers.add_parser(
        "save_if_changed", help="""Saves the modified text to the file if changes have been made.."""
    )

    save_if_changed_parser.add_argument("--file-path", dest="file_path", help="""The path to the file.""")

    save_if_changed_parser.add_argument("--final", dest="final", help="""The modified text.""")

    save_if_changed_parser.add_argument("--input-text", dest="input_text", help="""The original text.""")

    save_if_changed_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    save_if_changed_parser.set_defaults(func=save_if_changed_command)

    # Create a parser for the "revert_to_latest_backup" command
    revert_to_latest_backup_parser = subparsers.add_parser(
        "revert_to_latest_backup", help="""Revert the file to the most recent backup.."""
    )

    revert_to_latest_backup_parser.add_argument(
        "--file-name", dest="file_name", help="""The name of the file to revert."""
    )

    revert_to_latest_backup_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    revert_to_latest_backup_parser.set_defaults(func=revert_to_latest_backup_command)

    # Create a parser for the "rewrite_file" command
    rewrite_file_parser = subparsers.add_parser(
        "rewrite_file", help="""Backup and rewrite an existing file at file_path within the root_folder.."""
    )

    rewrite_file_parser.add_argument(
        "--file-path", dest="file_path", help="""The relative path to the file to be rewritten."""
    )

    rewrite_file_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    rewrite_file_parser.add_argument("--text", dest="text", help="""The new content to write into the file.""")
    rewrite_file_parser.set_defaults(func=rewrite_file_command)

    # Create a parser for the "write_new_file" command
    write_new_file_parser = subparsers.add_parser(
        "write_new_file", help="""Write a new file at file_path within the root_folder.."""
    )

    write_new_file_parser.add_argument(
        "--file-path", dest="file_path", help="""The relative path to the file to be written."""
    )

    write_new_file_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )

    write_new_file_parser.add_argument("--text", dest="text", help="""The content to write into the file.""")
    write_new_file_parser.set_defaults(func=write_new_file_command)

    # Create a parser for the "report_bool" command
    report_bool_parser = subparsers.add_parser("report_bool", help="""Report answer in bool format..""")

    report_bool_parser.add_argument(
        "--answer", dest="answer", action="store_true", help="""The answer to be reported in bool format."""
    )

    report_bool_parser.add_argument(
        "--comment", dest="comment", help="""Any comments, supplemental info about the answer."""
    )

    report_bool_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    report_bool_parser.set_defaults(func=report_bool_command)

    # Create a parser for the "report_dict" command
    report_dict_parser = subparsers.add_parser("report_dict", help="""Report answer in dict format..""")

    report_dict_parser.add_argument("--answer", dest="answer", help="""The answer to be reported in dict format.""")

    report_dict_parser.add_argument(
        "--comment", dest="comment", help="""Any comments, supplemental info about the answer."""
    )

    report_dict_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    report_dict_parser.set_defaults(func=report_dict_command)

    # Create a parser for the "report_float" command
    report_float_parser = subparsers.add_parser("report_float", help="""Report answer in string format..""")

    report_float_parser.add_argument("--answer", dest="answer", help="""The answer to be reported in float format.""")

    report_float_parser.add_argument(
        "--comment", dest="comment", help="""Any comments, supplemental info about the answer."""
    )

    report_float_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    report_float_parser.set_defaults(func=report_float_command)

    # Create a parser for the "report_int" command
    report_int_parser = subparsers.add_parser("report_int", help="""Report answer in integer format.""")

    report_int_parser.add_argument("--answer", dest="answer", help="""The answer to be reported in integer format.""")

    report_int_parser.add_argument(
        "--comment", dest="comment", help="""Any comments, supplemental info about the answer."""
    )

    report_int_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    report_int_parser.set_defaults(func=report_int_command)

    # Create a parser for the "report_json" command
    report_json_parser = subparsers.add_parser("report_json", help="""Report answer in json format..""")

    report_json_parser.add_argument("--answer", dest="answer", help="""The answer to be reported in json format.""")

    report_json_parser.add_argument(
        "--comment", dest="comment", help="""Any comments, supplemental info about the answer."""
    )

    report_json_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    report_json_parser.set_defaults(func=report_json_command)

    # Create a parser for the "report_list" command
    report_list_parser = subparsers.add_parser("report_list", help="""Report answer in list format..""")

    report_list_parser.add_argument("--answer", dest="answer", help="""The answer to be reported in list format.""")

    report_list_parser.add_argument(
        "--comment", dest="comment", help="""Any comments, supplemental info about the answer."""
    )

    report_list_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    report_list_parser.set_defaults(func=report_list_command)

    # Create a parser for the "report_set" command
    report_set_parser = subparsers.add_parser("report_set", help="""Report answer in set format..""")

    report_set_parser.add_argument("--answer", dest="answer", help="""The answer to be reported in set format.""")

    report_set_parser.add_argument(
        "--comment", dest="comment", help="""Any comments, supplemental info about the answer."""
    )

    report_set_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    report_set_parser.set_defaults(func=report_set_command)

    # Create a parser for the "report_text" command
    report_text_parser = subparsers.add_parser("report_text", help="""Report answer in string format..""")

    report_text_parser.add_argument("--answer", dest="answer", help="""The answer to be reported in string format.""")

    report_text_parser.add_argument(
        "--comment", dest="comment", help="""Any comments, supplemental info about the answer."""
    )

    report_text_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    report_text_parser.set_defaults(func=report_text_command)

    # Create a parser for the "report_toml" command
    report_toml_parser = subparsers.add_parser("report_toml", help="""Report answer in toml format..""")

    report_toml_parser.add_argument("--answer", dest="answer", help="""The answer to be reported in toml format.""")

    report_toml_parser.add_argument(
        "--comment", dest="comment", help="""Any comments, supplemental info about the answer."""
    )

    report_toml_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    report_toml_parser.set_defaults(func=report_toml_command)

    # Create a parser for the "report_tuple" command
    report_tuple_parser = subparsers.add_parser("report_tuple", help="""Report answer in tuple format..""")

    report_tuple_parser.add_argument("--answer", dest="answer", help="""The answer to be reported in tuple format.""")

    report_tuple_parser.add_argument(
        "--comment", dest="comment", help="""Any comments, supplemental info about the answer."""
    )

    report_tuple_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    report_tuple_parser.set_defaults(func=report_tuple_command)

    # Create a parser for the "report_xml" command
    report_xml_parser = subparsers.add_parser("report_xml", help="""Report answer in xml format..""")

    report_xml_parser.add_argument("--answer", dest="answer", help="""The answer to be reported in xml format.""")

    report_xml_parser.add_argument(
        "--comment", dest="comment", help="""Any comments, supplemental info about the answer."""
    )

    report_xml_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    report_xml_parser.set_defaults(func=report_xml_command)

    # Create a parser for the "pytest" command
    pytest_parser = subparsers.add_parser("pytest", help="""Runs pytest on tests in tests folder...""")

    pytest_parser.add_argument(
        "--mime-type",
        dest="mime_type",
        help="""Return value as text/csv, text/markdown, or text/yaml inside the JSON.""",
    )
    pytest_parser.set_defaults(func=pytest_command)

    # Parse the arguments
    args = parser.parse_args()

    # Execute the appropriate command
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    run()
