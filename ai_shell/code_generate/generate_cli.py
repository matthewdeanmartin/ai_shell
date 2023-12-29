"""
Code generate reverse client
"""
from typing import Any, cast

import ai_shell.openai_schemas as schemas


def generate_method_code(schema: dict, prologue: str):
    """
    Generates Python method code from a given JSON schema.

    Args:
    schema (dict): JSON schema dictionary.
    prologue (str): Prologue to be added to the method.

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
        "object": "Any",
        "array": "list",
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
            # Determine if argument is required or optional
            required = arg_name in required_args
            default_value = f"{arg_details['default']}" if "default" in arg_details else "= None"
            default_clause = default_value if not required else ""
            if default_clause and arg_details["type"] == "string":
                default_clause = f'"{default_clause}"'

            # Construct and append the cast line
            arg_type = arg_details["type"]
            python_type = type_mapping[arg_type]

            method_code += f"        {arg_name} = cast({python_type}, arguments.get('{arg_name}',{default_clause}))\n"

        # Method body (example with a placeholder for actual functionality)
        method_code += f"        return tool.{method_name}(\n"
        for arg_name in arguments.keys():
            method_code += f"            {arg_name}={arg_name},\n"
        method_code = method_code.rstrip(",\n") + "\n        )\n\n"

    return method_code


def generate_the_cli(target_file: str) -> None:
    """Main entry point.
    Args:
        target_file (str): The target file path for the generated code.
    """
    tools = ""
    for _ns, json_schema in schemas._SCHEMAS.items():
        for tool, _ in json_schema.items():
            tools += f'            "{tool}" : self.{tool},\n'

    meta: dict[str, dict[str, str]] = {}
    meta["headtail"] = {
        "module": "ai_shell.head_tail_tool",
        "class": "HeadTailTool",
    }
    meta["cat"] = {
        "module": "ai_shell.cat_tool",
        "class": "CatTool",
    }
    meta["cut"] = {
        "module": "ai_shell.cut_tool",
        "class": "CutTool",
    }
    meta["find"] = {
        "module": "ai_shell.find_tool",
        "class": "FindTool",
    }
    meta["git"] = {
        "module": "ai_shell.git_tool",
        "class": "GitTool",
    }
    meta["patch"] = {
        "module": "ai_shell.patch_tool",
        "class": "PatchTool",
    }
    meta["ls"] = {
        "module": "ai_shell.ls_tool",
        "class": "LsTool",
    }
    meta["grep"] = {
        "module": "ai_shell.grep_tool",
        "class": "GrepTool",
    }
    meta["token_counter"] = {
        "module": "ai_shell.token_tool",
        "class": "TokenCounterTool",
    }
    meta["todo"] = {
        "module": "ai_shell.todo_tool",
        "class": "TodoTool",
    }
    meta["insert"] = {
        "module": "ai_shell.insert_tool",
        "class": "InsertTool",
    }
    meta["replace"] = {
        "module": "ai_shell.replace_tool",
        "class": "ReplaceTool",
    }
    meta["rewrite"] = {
        "module": "ai_shell.rewrite_tool",
        "class": "RewriteTool",
    }
    meta["answer_collector"] = {
        "module": "ai_shell.answer_tool",
        "class": "AnswerCollectorTool",
    }
    meta["pytest"] = {
        "module": "ai_shell.pytest_tool",
        "class": "PytestTool",
    }

    header = """\"\"\"
Generated code, do not edit.
\"\"\"
import argparse
from ai_shell.utils.console_utils import pretty_console
from ai_shell.utils.config_manager import Config

CONFIG = Config()
# pylint: disable=unused-argument
"""

    for _key, value in meta.items():
        header += f"\nfrom {value['module']} import {value['class']}"
    header += "\n\n"

    middle = ""
    for ns, data in meta.items():
        middle += "\n"
        for method, method_data in schemas._SCHEMAS[ns].items():
            middle += "\n"
            middle += f"def {method}_command(args):\n"
            middle += f'    """Invoke {method}"""\n'
            middle += f"    tool = {data['class']}('.', CONFIG)\n"
            middle += f"    pretty_console(tool.{method}("
            for arg_name, _arg_details in cast(dict[str, Any], method_data["properties"]).items():
                if arg_name != "mime_type":
                    # don't know how to handle mime types in CLI yet.
                    middle += f"\n        {arg_name} = args.{arg_name},"
            middle += "\n    ))"

    argparse_part = """\n\ndef run():
        \"\"\"Create the main parser\"\"\"
        parser = argparse.ArgumentParser(prog='ais', description='AI Shell Command Line Interface')
        subparsers = parser.add_subparsers(dest='subcommand', help='sub-command help')
    """
    for ns, _data in meta.items():
        for method, method_data in schemas._SCHEMAS[ns].items():
            escaped_method_description = (
                cast(str, method_data.get("description", "")).replace("'", "\\'").replace("\n", "\\n")
            )
            argparse_part += f'    # Create a parser for the "{method}" command\n'
            argparse_part += f"""    {method}_parser = subparsers.add_parser('{method}', help=\"\"\"{escaped_method_description}.\"\"\")\n"""
            for arg_name, arg_details in cast(dict[str, Any], method_data["properties"]).items():
                dashed_arg_name = arg_name.replace("_", "-")
                escaped_description = arg_details.get("description", "").replace("'", "\\'")

                argparse_part += f"\n    {method}_parser.add_argument('--{dashed_arg_name}', "
                bool_part = ""
                if arg_details["type"] == "boolean":
                    bool_part = "action='store_true', "

                if method_data.get("default"):
                    argparse_part += (
                        f"    dest='{arg_name}', {bool_part} default={method_data['default']},\n"
                        f"    help='{escaped_description}, defaults to {method_data['default']}')\n"
                    )
                else:
                    argparse_part += f'    dest=\'{arg_name}\', {bool_part} help="""{escaped_description}""")\n'

                # if list
                # cat_parser.add_argument('file_paths', nargs='+', type=str, help='Paths to the files to be concatenated')

            argparse_part += f"    {method}_parser.set_defaults(func={method}_command)\n\n"

    argparse_part += """        # Parse the arguments
        args = parser.parse_args()
    """

    footer = """
    # Execute the appropriate command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    run()
"""

    # Generate method code
    with open(target_file, "w", encoding="utf-8") as code:
        code.write(header)
        code.write(middle)
        code.write(argparse_part)
        code.write(footer)


if __name__ == "__main__":
    generate_the_cli(target_file="../../ai_shell/__main__.py")
