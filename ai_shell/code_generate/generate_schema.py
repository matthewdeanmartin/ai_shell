"""
Generates JsonSchema in form of a python file.
"""
import logging
from pprint import pformat

import ai_shell
from ai_shell.code_generate.method_to_jsonschema import convert_to_json_schema


def generate_the_schema(target_file: str) -> None:
    """Main entrypoint.

    Args:
        target_file (str): The target file path for the generated code.
    """
    # Setup logging for my_app
    # We will only setup a console handler
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(ch)

    schemas = {}
    schemas["cat"] = convert_to_json_schema(ai_shell.CatTool)
    schemas["cut"] = convert_to_json_schema(ai_shell.CutTool)
    schemas["ed"] = convert_to_json_schema(ai_shell.EdTool)
    schemas["sed"] = convert_to_json_schema(ai_shell.SedTool)
    schemas["insert"] = convert_to_json_schema(ai_shell.InsertTool)
    schemas["replace"] = convert_to_json_schema(ai_shell.ReplaceTool)
    schemas["headtail"] = convert_to_json_schema(ai_shell.HeadTailTool)
    schemas["edlin"] = convert_to_json_schema(ai_shell.EdlinTool)
    schemas["find"] = convert_to_json_schema(ai_shell.FindTool)
    schemas["git"] = convert_to_json_schema(ai_shell.GitTool)
    schemas["patch"] = convert_to_json_schema(ai_shell.PatchTool)
    schemas["ls"] = convert_to_json_schema(ai_shell.LsTool)
    schemas["grep"] = convert_to_json_schema(ai_shell.GrepTool)
    schemas["pycat"] = convert_to_json_schema(ai_shell.PyCatTool)
    schemas["token_counter"] = convert_to_json_schema(ai_shell.TokenCounterTool)
    schemas["todo"] = convert_to_json_schema(ai_shell.TodoTool)
    schemas["answer_collector"] = convert_to_json_schema(ai_shell.AnswerCollectorTool)
    schemas["rewrite"] = convert_to_json_schema(ai_shell.RewriteTool)
    schemas["pytest"] = convert_to_json_schema(ai_shell.PytestTool)

    with open(target_file, "w", encoding="utf-8") as source:
        source.write('"""jsonschema for functions"""')
        source.write("\n\n")
        source.write(f"_SCHEMAS = {pformat(schemas, indent=2)}")


if __name__ == "__main__":
    generate_the_schema("../../ai_shell/openai_schemas.py")
