"""
Code generate reverse client
"""

import ai_shell.openai_schemas as schemas


def generate_method_code(schema: dict, prologue: str, namespace: str):
    """
    Generates Python method code from a given JSON schema.

    Args:
    schema (dict): JSON schema dictionary.
    prologue (str): Prologue to be added to the method.
    namespace (str): Namespace of the tool.

    Returns:
    str: Generated Python method code.
    """
    method_code = ""
    type_mapping = {
        "integer": "int",
        "number": "float",
        "string": "str",
        "boolean": "bool",
        "null": "None",
        "object": "Any",  # dict[str,Any] ?
        "['object']": "Any",
        "list": "List[Any]",
        "array": "list[Any]",
        "['string', 'null']": "Optional[str]",
        "['integer', 'null']": "Optional[int]",
        "['number', 'null']": "Optional[float]",
    }
    for method_name, details in schema.items():
        arguments = details["properties"]
        required_args = details.get("required", [])
        # return_type = type_mapping.get(details["type"],details["type"])
        # Json Schema doesn't know type of return value! Because this schema was never meant for `Callable`
        return_type = "Any"

        # Start method definition
        method_code += (
            f"    def {method_name}(self, arguments: dict[str, Any]) -> {return_type}:\n"
            f'        """Generated Do Not Edit"""\n'
            f"        {prologue}\n\n"
        )

        # Generate code for each argument
        for arg_name, arg_details in arguments.items():
            if arg_name == "mime_type":
                continue
            # Determine if argument is required or optional
            required = arg_name in required_args
            default_value = f"{arg_details['default']}" if "default" in arg_details else "= None"
            default_clause = default_value if not required else ""
            if default_clause and "string" in arg_details["type"]:
                default_clause = f'"{default_clause}"'

            # Construct and append the cast line
            arg_type = arg_details["type"]
            python_type = type_mapping[str(arg_type)]
            method_code += f"        {arg_name} = cast({python_type}, arguments.get('{arg_name}',{default_clause}))\n"

        if "self.tool" in prologue:
            method_code += f"        return self.tool_{namespace}.{method_name}(\n"
        else:
            method_code += f"        return tool.{method_name}(\n"

        for arg_name in arguments.keys():
            if arg_name == "mime_type":
                continue
            method_code += f"            {arg_name}={arg_name},\n"
        method_code = method_code.rstrip(",\n") + "\n        )\n\n"

    return method_code


def generate_the_toolkit(target_file: str) -> None:
    """Main entry point
    Args:
        target_file (str): Target file to write the generated code.
    """
    tools = ""
    for _ns, json_schema in schemas._SCHEMAS.items():
        for tool, _ in json_schema.items():
            tools += f'            "{tool}" : self.{tool},\n'

    header = f"""\"\"\"
Generate code, do not edit.
\"\"\"
from ai_shell.openai_support import ToolKitBase
from typing import Any, cast, Callable, Optional

from ai_shell.cat_tool import CatTool
from ai_shell.find_tool import FindTool
from ai_shell.git_tool import GitTool
from ai_shell.grep_tool import GrepTool
from ai_shell.ls_tool import LsTool
from ai_shell.token_tool import TokenCounterTool
from ai_shell.edlin_tool import EdlinTool
from ai_shell.pycat_tool import PyCatTool
from ai_shell.ed_tool import EdTool
from ai_shell.cut_tool import CutTool
from ai_shell.head_tail_tool import HeadTailTool
from ai_shell.patch_tool import PatchTool
from ai_shell.sed_tool import SedTool
from ai_shell.insert_tool import InsertTool
from ai_shell.replace_tool import ReplaceTool
from ai_shell.todo_tool import TodoTool
from ai_shell.answer_tool import AnswerCollectorTool
from ai_shell.rewrite_tool import RewriteTool
from ai_shell.pytest_tool import PytestTool

# pylint: disable=unused-argument

class ToolKit(ToolKitBase):
    \"\"\"AI Shell Toolkit\"\"\"\n\n
    def __init__(self, root_folder: str, token_model: str, global_max_lines: int, permitted_tools: list[str], config:Config) -> None:
        super().__init__(root_folder, token_model, global_max_lines, permitted_tools, config)
        self._lookup: dict[str, Callable[[dict[str, Any]], Any]] = {{
            {tools}
        }}
        # Stateful tool support
        self.tool_answer_collector = None
"""

    prologue = {}
    prologue["cat"] = "tool = CatTool(self.root_folder, self.config)"
    prologue["headtail"] = "tool = HeadTailTool(self.root_folder, self.config)"
    prologue["cut"] = "tool = CutTool(self.root_folder, self.config)"
    prologue["pycat"] = "tool = PyCatTool(self.root_folder, self.config)"
    prologue["ed"] = "tool = EdTool(self.root_folder, self.config)"
    prologue["sed"] = "tool = SedTool(self.root_folder, self.config)"
    prologue["insert"] = "tool = InsertTool(self.root_folder, self.config)"
    prologue["replace"] = "tool = ReplaceTool(self.root_folder, self.config)"
    prologue["edlin"] = "tool = EdlinTool(self.root_folder, self.config)"
    prologue["find"] = "tool = FindTool(self.root_folder, self.config)"
    prologue["git"] = "tool = GitTool(self.root_folder, self.config)"
    prologue["patch"] = "tool = PatchTool(self.root_folder, self.config)"
    prologue["ls"] = "tool = LsTool(self.root_folder, self.config)"
    prologue["grep"] = "tool = GrepTool(self.root_folder, self.config)"
    prologue["token_counter"] = "tool = TokenCounterTool(self.root_folder, self.config)"  # nosec
    prologue["todo"] = "tool = TodoTool(self.root_folder, self.config)"
    prologue["answer_collector"] = (
        "if not self.tool_answer_collector:\n"
        "            raise TypeError('tool cannot be None here')\n\n"
        "        self.tool_answer_collector = AnswerCollectorTool(self.root_folder, self.config)"
    )
    prologue["rewrite"] = "tool = RewriteTool(self.root_folder, self.config)"
    prologue["pytest"] = "tool = PytestTool(self.root_folder, self.config)"

    # Generate method code
    with open(target_file, "w", encoding="utf-8") as code:
        code.write(header)
        for ns, json_schema in schemas._SCHEMAS.items():
            pro = prologue[ns]
            method_code = generate_method_code(json_schema, pro, ns)
            code.write(method_code)


if __name__ == "__main__":
    generate_the_toolkit("../../ai_shell/openai_toolkit.py")
