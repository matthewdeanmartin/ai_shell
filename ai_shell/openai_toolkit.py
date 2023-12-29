"""
Generate code, do not edit.
"""
from collections.abc import Callable
from typing import Any, Optional, cast

from ai_shell.answer_tool import AnswerCollectorTool
from ai_shell.cat_tool import CatTool
from ai_shell.cut_tool import CutTool
from ai_shell.ed_tool import EdTool
from ai_shell.edlin_tool import EdlinTool
from ai_shell.find_tool import FindTool
from ai_shell.git_tool import GitTool
from ai_shell.grep_tool import GrepTool
from ai_shell.head_tail_tool import HeadTailTool
from ai_shell.insert_tool import InsertTool
from ai_shell.ls_tool import LsTool
from ai_shell.openai_support import ToolKitBase
from ai_shell.patch_tool import PatchTool
from ai_shell.pycat_tool import PyCatTool
from ai_shell.pytest_tool import PytestTool
from ai_shell.replace_tool import ReplaceTool
from ai_shell.rewrite_tool import RewriteTool
from ai_shell.sed_tool import SedTool
from ai_shell.todo_tool import TodoTool
from ai_shell.token_tool import TokenCounterTool
from ai_shell.utils.config_manager import Config

# pylint: disable=unused-argument


class ToolKit(ToolKitBase):
    """AI Shell Toolkit"""

    def __init__(
        self, root_folder: str, token_model: str, global_max_lines: int, permitted_tools: list[str], config: Config
    ) -> None:
        super().__init__(root_folder, token_model, global_max_lines, permitted_tools, config)
        self._lookup: dict[str, Callable[[dict[str, Any]], Any]] = {
            "report_bool": self.report_bool,
            "report_dict": self.report_dict,
            "report_float": self.report_float,
            "report_int": self.report_int,
            "report_json": self.report_json,
            "report_list": self.report_list,
            "report_set": self.report_set,
            "report_text": self.report_text,
            "report_toml": self.report_toml,
            "report_tuple": self.report_tuple,
            "report_xml": self.report_xml,
            "cat": self.cat,
            "cat_markdown": self.cat_markdown,
            "cut_characters": self.cut_characters,
            "cut_fields": self.cut_fields,
            "cut_fields_by_name": self.cut_fields_by_name,
            "ed": self.ed,
            "edlin": self.edlin,
            "find_files": self.find_files,
            "find_files_markdown": self.find_files_markdown,
            "get_current_branch": self.get_current_branch,
            "get_recent_commits": self.get_recent_commits,
            "git_diff": self.git_diff,
            "git_diff_commit": self.git_diff_commit,
            "git_log_file": self.git_log_file,
            "git_log_search": self.git_log_search,
            "git_show": self.git_show,
            "git_status": self.git_status,
            "is_ignored_by_gitignore": self.is_ignored_by_gitignore,
            "grep": self.grep,
            "grep_markdown": self.grep_markdown,
            "head": self.head,
            "head_markdown": self.head_markdown,
            "head_tail": self.head_tail,
            "tail": self.tail,
            "tail_markdown": self.tail_markdown,
            "insert_text_after_context": self.insert_text_after_context,
            "insert_text_after_multiline_context": self.insert_text_after_multiline_context,
            "insert_text_at_start_or_end": self.insert_text_at_start_or_end,
            "ls": self.ls,
            "ls_markdown": self.ls_markdown,
            "apply_git_patch": self.apply_git_patch,
            "format_code_as_markdown": self.format_code_as_markdown,
            "pytest": self.pytest,
            "replace_all": self.replace_all,
            "replace_line_by_line": self.replace_line_by_line,
            "replace_with_regex": self.replace_with_regex,
            "save_if_changed": self.save_if_changed,
            "revert_to_latest_backup": self.revert_to_latest_backup,
            "rewrite_file": self.rewrite_file,
            "write_new_file": self.write_new_file,
            "sed": self.sed,
            "add_todo": self.add_todo,
            "query_todos_by_assignee": self.query_todos_by_assignee,
            "query_todos_by_regex": self.query_todos_by_regex,
            "remove_todo": self.remove_todo,
            "count_tokens": self.count_tokens,
        }
        # Stateful tool support
        self.tool_answer_collector = None

    def report_bool(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        if not self.tool_answer_collector:
            raise TypeError("tool cannot be None here")

        self.tool_answer_collector = AnswerCollectorTool(self.root_folder, self.config)

        answer = cast(
            bool,
            arguments.get(
                "answer",
            ),
        )
        comment = cast(
            str,
            arguments.get(
                "comment",
            ),
        )
        return self.tool_answer_collector.report_bool(answer=answer, comment=comment)

    def report_dict(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        if not self.tool_answer_collector:
            raise TypeError("tool cannot be None here")

        self.tool_answer_collector = AnswerCollectorTool(self.root_folder, self.config)

        answer = cast(
            Any,
            arguments.get(
                "answer",
            ),
        )
        comment = cast(
            str,
            arguments.get(
                "comment",
            ),
        )
        return self.tool_answer_collector.report_dict(answer=answer, comment=comment)

    def report_float(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        if not self.tool_answer_collector:
            raise TypeError("tool cannot be None here")

        self.tool_answer_collector = AnswerCollectorTool(self.root_folder, self.config)

        answer = cast(
            float,
            arguments.get(
                "answer",
            ),
        )
        comment = cast(
            str,
            arguments.get(
                "comment",
            ),
        )
        return self.tool_answer_collector.report_float(answer=answer, comment=comment)

    def report_int(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        if not self.tool_answer_collector:
            raise TypeError("tool cannot be None here")

        self.tool_answer_collector = AnswerCollectorTool(self.root_folder, self.config)

        answer = cast(
            int,
            arguments.get(
                "answer",
            ),
        )
        comment = cast(
            str,
            arguments.get(
                "comment",
            ),
        )
        return self.tool_answer_collector.report_int(answer=answer, comment=comment)

    def report_json(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        if not self.tool_answer_collector:
            raise TypeError("tool cannot be None here")

        self.tool_answer_collector = AnswerCollectorTool(self.root_folder, self.config)

        answer = cast(
            str,
            arguments.get(
                "answer",
            ),
        )
        comment = cast(
            str,
            arguments.get(
                "comment",
            ),
        )
        return self.tool_answer_collector.report_json(answer=answer, comment=comment)

    def report_list(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        if not self.tool_answer_collector:
            raise TypeError("tool cannot be None here")

        self.tool_answer_collector = AnswerCollectorTool(self.root_folder, self.config)

        answer = cast(
            str,
            arguments.get(
                "answer",
            ),
        )
        comment = cast(
            str,
            arguments.get(
                "comment",
            ),
        )
        return self.tool_answer_collector.report_list(answer=answer, comment=comment)

    def report_set(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        if not self.tool_answer_collector:
            raise TypeError("tool cannot be None here")

        self.tool_answer_collector = AnswerCollectorTool(self.root_folder, self.config)

        answer = cast(
            list[Any],
            arguments.get(
                "answer",
            ),
        )
        comment = cast(
            str,
            arguments.get(
                "comment",
            ),
        )
        return self.tool_answer_collector.report_set(answer=answer, comment=comment)

    def report_text(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        if not self.tool_answer_collector:
            raise TypeError("tool cannot be None here")

        self.tool_answer_collector = AnswerCollectorTool(self.root_folder, self.config)

        answer = cast(
            str,
            arguments.get(
                "answer",
            ),
        )
        comment = cast(
            str,
            arguments.get(
                "comment",
            ),
        )
        return self.tool_answer_collector.report_text(answer=answer, comment=comment)

    def report_toml(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        if not self.tool_answer_collector:
            raise TypeError("tool cannot be None here")

        self.tool_answer_collector = AnswerCollectorTool(self.root_folder, self.config)

        answer = cast(
            str,
            arguments.get(
                "answer",
            ),
        )
        comment = cast(
            str,
            arguments.get(
                "comment",
            ),
        )
        return self.tool_answer_collector.report_toml(answer=answer, comment=comment)

    def report_tuple(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        if not self.tool_answer_collector:
            raise TypeError("tool cannot be None here")

        self.tool_answer_collector = AnswerCollectorTool(self.root_folder, self.config)

        answer = cast(
            list[Any],
            arguments.get(
                "answer",
            ),
        )
        comment = cast(
            str,
            arguments.get(
                "comment",
            ),
        )
        return self.tool_answer_collector.report_tuple(answer=answer, comment=comment)

    def report_xml(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        if not self.tool_answer_collector:
            raise TypeError("tool cannot be None here")

        self.tool_answer_collector = AnswerCollectorTool(self.root_folder, self.config)

        answer = cast(
            str,
            arguments.get(
                "answer",
            ),
        )
        comment = cast(
            str,
            arguments.get(
                "comment",
            ),
        )
        return self.tool_answer_collector.report_xml(answer=answer, comment=comment)

    def cat(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = CatTool(self.root_folder, self.config)

        file_paths = cast(
            str,
            arguments.get(
                "file_paths",
            ),
        )
        number_lines = cast(bool, arguments.get("number_lines", True))
        squeeze_blank = cast(bool, arguments.get("squeeze_blank", False))
        return tool.cat(file_paths=file_paths, number_lines=number_lines, squeeze_blank=squeeze_blank)

    def cat_markdown(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = CatTool(self.root_folder, self.config)

        file_paths = cast(
            str,
            arguments.get(
                "file_paths",
            ),
        )
        number_lines = cast(bool, arguments.get("number_lines", True))
        squeeze_blank = cast(bool, arguments.get("squeeze_blank", False))
        return tool.cat_markdown(file_paths=file_paths, number_lines=number_lines, squeeze_blank=squeeze_blank)

    def cut_characters(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = CutTool(self.root_folder, self.config)

        character_ranges = cast(
            str,
            arguments.get(
                "character_ranges",
            ),
        )
        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        return tool.cut_characters(character_ranges=character_ranges, file_path=file_path)

    def cut_fields(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = CutTool(self.root_folder, self.config)

        delimiter = cast(str, arguments.get("delimiter", ","))
        field_ranges = cast(
            str,
            arguments.get(
                "field_ranges",
            ),
        )
        filename = cast(
            str,
            arguments.get(
                "filename",
            ),
        )
        return tool.cut_fields(delimiter=delimiter, field_ranges=field_ranges, filename=filename)

    def cut_fields_by_name(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = CutTool(self.root_folder, self.config)

        delimiter = cast(str, arguments.get("delimiter", ","))
        field_names = cast(
            str,
            arguments.get(
                "field_names",
            ),
        )
        filename = cast(
            str,
            arguments.get(
                "filename",
            ),
        )
        return tool.cut_fields_by_name(delimiter=delimiter, field_names=field_names, filename=filename)

    def ed(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = EdTool(self.root_folder, self.config)

        file_name = cast(
            str,
            arguments.get(
                "file_name",
            ),
        )
        script = cast(
            str,
            arguments.get(
                "script",
            ),
        )
        return tool.ed(file_name=file_name, script=script)

    def edlin(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = EdlinTool(self.root_folder, self.config)

        file_name = cast(
            str,
            arguments.get(
                "file_name",
            ),
        )
        script = cast(
            str,
            arguments.get(
                "script",
            ),
        )
        return tool.edlin(file_name=file_name, script=script)

    def find_files(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = FindTool(self.root_folder, self.config)

        file_type = cast(
            Optional[str],
            arguments.get(
                "file_type",
            ),
        )
        name = cast(
            Optional[str],
            arguments.get(
                "name",
            ),
        )
        regex = cast(
            Optional[str],
            arguments.get(
                "regex",
            ),
        )
        size = cast(
            Optional[str],
            arguments.get(
                "size",
            ),
        )
        return tool.find_files(file_type=file_type, name=name, regex=regex, size=size)

    def find_files_markdown(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = FindTool(self.root_folder, self.config)

        file_type = cast(
            Optional[str],
            arguments.get(
                "file_type",
            ),
        )
        name = cast(
            Optional[str],
            arguments.get(
                "name",
            ),
        )
        regex = cast(
            Optional[str],
            arguments.get(
                "regex",
            ),
        )
        size = cast(
            Optional[str],
            arguments.get(
                "size",
            ),
        )
        return tool.find_files_markdown(file_type=file_type, name=name, regex=regex, size=size)

    def get_current_branch(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = GitTool(self.root_folder, self.config)

        return tool.get_current_branch()

    def get_recent_commits(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = GitTool(self.root_folder, self.config)

        n = cast(int, arguments.get("n", 10))
        short_hash = cast(bool, arguments.get("short_hash", False))
        return tool.get_recent_commits(n=n, short_hash=short_hash)

    def git_diff(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = GitTool(self.root_folder, self.config)

        return tool.git_diff()

    def git_diff_commit(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = GitTool(self.root_folder, self.config)

        commit1 = cast(
            str,
            arguments.get(
                "commit1",
            ),
        )
        commit2 = cast(
            str,
            arguments.get(
                "commit2",
            ),
        )
        return tool.git_diff_commit(commit1=commit1, commit2=commit2)

    def git_log_file(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = GitTool(self.root_folder, self.config)

        filename = cast(
            str,
            arguments.get(
                "filename",
            ),
        )
        return tool.git_log_file(filename=filename)

    def git_log_search(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = GitTool(self.root_folder, self.config)

        search_string = cast(
            str,
            arguments.get(
                "search_string",
            ),
        )
        return tool.git_log_search(search_string=search_string)

    def git_show(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = GitTool(self.root_folder, self.config)

        return tool.git_show()

    def git_status(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = GitTool(self.root_folder, self.config)

        return tool.git_status()

    def is_ignored_by_gitignore(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = GitTool(self.root_folder, self.config)

        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        gitignore_path = cast(str, arguments.get("gitignore_path", ".gitignore"))
        return tool.is_ignored_by_gitignore(file_path=file_path, gitignore_path=gitignore_path)

    def grep(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = GrepTool(self.root_folder, self.config)

        glob_pattern = cast(
            str,
            arguments.get(
                "glob_pattern",
            ),
        )
        maximum_matches_per_file = cast(int, arguments.get("maximum_matches_per_file", -1))
        maximum_matches_total = cast(int, arguments.get("maximum_matches_total", -1))
        regex = cast(
            str,
            arguments.get(
                "regex",
            ),
        )
        skip_first_matches = cast(int, arguments.get("skip_first_matches", -1))
        return tool.grep(
            glob_pattern=glob_pattern,
            maximum_matches_per_file=maximum_matches_per_file,
            maximum_matches_total=maximum_matches_total,
            regex=regex,
            skip_first_matches=skip_first_matches,
        )

    def grep_markdown(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = GrepTool(self.root_folder, self.config)

        glob_pattern = cast(
            str,
            arguments.get(
                "glob_pattern",
            ),
        )
        maximum_matches = cast(int, arguments.get("maximum_matches", -1))
        regex = cast(
            str,
            arguments.get(
                "regex",
            ),
        )
        skip_first_matches = cast(int, arguments.get("skip_first_matches", -1))
        return tool.grep_markdown(
            glob_pattern=glob_pattern,
            maximum_matches=maximum_matches,
            regex=regex,
            skip_first_matches=skip_first_matches,
        )

    def head(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = HeadTailTool(self.root_folder, self.config)

        byte_count = cast(
            Optional[int],
            arguments.get(
                "byte_count",
            ),
        )
        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        lines = cast(int, arguments.get("lines", 10))
        return tool.head(byte_count=byte_count, file_path=file_path, lines=lines)

    def head_markdown(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = HeadTailTool(self.root_folder, self.config)

        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        lines = cast(int, arguments.get("lines", 10))
        return tool.head_markdown(file_path=file_path, lines=lines)

    def head_tail(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = HeadTailTool(self.root_folder, self.config)

        byte_count = cast(
            Optional[int],
            arguments.get(
                "byte_count",
            ),
        )
        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        lines = cast(int, arguments.get("lines", 10))
        mode = cast(str, arguments.get("mode", "head"))
        return tool.head_tail(byte_count=byte_count, file_path=file_path, lines=lines, mode=mode)

    def tail(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = HeadTailTool(self.root_folder, self.config)

        byte_count = cast(
            Optional[int],
            arguments.get(
                "byte_count",
            ),
        )
        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        lines = cast(int, arguments.get("lines", 10))
        return tool.tail(byte_count=byte_count, file_path=file_path, lines=lines)

    def tail_markdown(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = HeadTailTool(self.root_folder, self.config)

        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        lines = cast(int, arguments.get("lines", 10))
        return tool.tail_markdown(file_path=file_path, lines=lines)

    def insert_text_after_context(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = InsertTool(self.root_folder, self.config)

        context = cast(
            str,
            arguments.get(
                "context",
            ),
        )
        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        text_to_insert = cast(
            str,
            arguments.get(
                "text_to_insert",
            ),
        )
        return tool.insert_text_after_context(context=context, file_path=file_path, text_to_insert=text_to_insert)

    def insert_text_after_multiline_context(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = InsertTool(self.root_folder, self.config)

        context_lines = cast(
            str,
            arguments.get(
                "context_lines",
            ),
        )
        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        text_to_insert = cast(
            str,
            arguments.get(
                "text_to_insert",
            ),
        )
        return tool.insert_text_after_multiline_context(
            context_lines=context_lines, file_path=file_path, text_to_insert=text_to_insert
        )

    def insert_text_at_start_or_end(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = InsertTool(self.root_folder, self.config)

        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        position = cast(str, arguments.get("position", "end"))
        text_to_insert = cast(
            str,
            arguments.get(
                "text_to_insert",
            ),
        )
        return tool.insert_text_at_start_or_end(file_path=file_path, position=position, text_to_insert=text_to_insert)

    def ls(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = LsTool(self.root_folder, self.config)

        all_files = cast(bool, arguments.get("all_files", False))
        long = cast(bool, arguments.get("long", False))
        path = cast(
            Optional[str],
            arguments.get(
                "path",
            ),
        )
        return tool.ls(all_files=all_files, long=long, path=path)

    def ls_markdown(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = LsTool(self.root_folder, self.config)

        all_files = cast(bool, arguments.get("all_files", False))
        long = cast(bool, arguments.get("long", False))
        path = cast(Optional[str], arguments.get("path", "."))
        return tool.ls_markdown(all_files=all_files, long=long, path=path)

    def apply_git_patch(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = PatchTool(self.root_folder, self.config)

        patch_content = cast(
            str,
            arguments.get(
                "patch_content",
            ),
        )
        return tool.apply_git_patch(patch_content=patch_content)

    def format_code_as_markdown(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = PyCatTool(self.root_folder, self.config)

        base_path = cast(
            str,
            arguments.get(
                "base_path",
            ),
        )
        header = cast(
            str,
            arguments.get(
                "header",
            ),
        )
        no_comments = cast(bool, arguments.get("no_comments", False))
        no_docs = cast(bool, arguments.get("no_docs", False))
        return tool.format_code_as_markdown(
            base_path=base_path, header=header, no_comments=no_comments, no_docs=no_docs
        )

    def pytest(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = PytestTool(self.root_folder, self.config)

        return tool.pytest()

    def replace_all(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = ReplaceTool(self.root_folder, self.config)

        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        new_text = cast(
            str,
            arguments.get(
                "new_text",
            ),
        )
        old_text = cast(
            str,
            arguments.get(
                "old_text",
            ),
        )
        return tool.replace_all(file_path=file_path, new_text=new_text, old_text=old_text)

    def replace_line_by_line(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = ReplaceTool(self.root_folder, self.config)

        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        line_end = cast(int, arguments.get("line_end", -1))
        line_start = cast(int, arguments.get("line_start", 0))
        new_text = cast(
            str,
            arguments.get(
                "new_text",
            ),
        )
        old_text = cast(
            str,
            arguments.get(
                "old_text",
            ),
        )
        return tool.replace_line_by_line(
            file_path=file_path, line_end=line_end, line_start=line_start, new_text=new_text, old_text=old_text
        )

    def replace_with_regex(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = ReplaceTool(self.root_folder, self.config)

        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        regex_match_expression = cast(
            str,
            arguments.get(
                "regex_match_expression",
            ),
        )
        replacement = cast(
            str,
            arguments.get(
                "replacement",
            ),
        )
        return tool.replace_with_regex(
            file_path=file_path, regex_match_expression=regex_match_expression, replacement=replacement
        )

    def save_if_changed(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = ReplaceTool(self.root_folder, self.config)

        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        final = cast(
            str,
            arguments.get(
                "final",
            ),
        )
        input_text = cast(
            str,
            arguments.get(
                "input_text",
            ),
        )
        return tool.save_if_changed(file_path=file_path, final=final, input_text=input_text)

    def revert_to_latest_backup(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = RewriteTool(self.root_folder, self.config)

        file_name = cast(
            str,
            arguments.get(
                "file_name",
            ),
        )
        return tool.revert_to_latest_backup(file_name=file_name)

    def rewrite_file(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = RewriteTool(self.root_folder, self.config)

        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        text = cast(
            str,
            arguments.get(
                "text",
            ),
        )
        return tool.rewrite_file(file_path=file_path, text=text)

    def write_new_file(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = RewriteTool(self.root_folder, self.config)

        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        text = cast(
            str,
            arguments.get(
                "text",
            ),
        )
        return tool.write_new_file(file_path=file_path, text=text)

    def sed(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = SedTool(self.root_folder, self.config)

        commands = cast(
            str,
            arguments.get(
                "commands",
            ),
        )
        file_path = cast(
            str,
            arguments.get(
                "file_path",
            ),
        )
        return tool.sed(commands=commands, file_path=file_path)

    def add_todo(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = TodoTool(self.root_folder, self.config)

        assignee = cast(
            Optional[str],
            arguments.get(
                "assignee",
            ),
        )
        category = cast(
            str,
            arguments.get(
                "category",
            ),
        )
        description = cast(
            str,
            arguments.get(
                "description",
            ),
        )
        source_code_ref = cast(
            str,
            arguments.get(
                "source_code_ref",
            ),
        )
        title = cast(
            str,
            arguments.get(
                "title",
            ),
        )
        return tool.add_todo(
            assignee=assignee, category=category, description=description, source_code_ref=source_code_ref, title=title
        )

    def query_todos_by_assignee(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = TodoTool(self.root_folder, self.config)

        return tool.query_todos_by_assignee()

    def query_todos_by_regex(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = TodoTool(self.root_folder, self.config)

        regex_pattern = cast(str, arguments.get("regex_pattern", r"[\s\S]+"))
        return tool.query_todos_by_regex(regex_pattern=regex_pattern)

    def remove_todo(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = TodoTool(self.root_folder, self.config)

        title = cast(
            str,
            arguments.get(
                "title",
            ),
        )
        return tool.remove_todo(title=title)

    def count_tokens(self, arguments: dict[str, Any]) -> Any:
        """Generated Do Not Edit"""
        tool = TokenCounterTool(self.root_folder, self.config)

        text = cast(
            str,
            arguments.get(
                "text",
            ),
        )
        return tool.count_tokens(text=text)
