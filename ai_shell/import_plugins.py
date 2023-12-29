import importlib
import os
import random
from typing import Any

from ai_shell.code_generate.method_to_jsonschema import convert_to_json_schema


def generate_data_for_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """
    Generates test data for a schema.

    Args:
        schema (dict[str, Any]): The schema to generate test data for.

    Returns:
        dict[str, Any]: The test data.
    """
    data = {}

    properties = schema.get("properties", {})
    required = schema.get("required", [])

    for prop, details in properties.items():
        prop_type = details.get("type")

        value: Any
        if prop_type == "string":
            value = "example_string" if prop != "mime_type" else "text/csv"
        elif prop_type == "integer":
            value = random.randint(0, 100)  # nosec
        elif prop_type == "number":
            value = random.uniform(0.0, 100.0)  # nosec
        else:
            value = None

        if prop in required or random.choice([True, False]):  # nosec
            data[prop] = value

    return data


def convert_to_toolkit(plugin_directory: str, root_folder: str) -> dict[str, Any]:
    """
    Converts all tools in a plugin directory to a toolkit.

    Args:
        plugin_directory (str): The directory to search for plugins.
        root_folder (str): The root folder of the workspace.

    Returns:
        dict[str, Any]: The toolkit metadata.
    """
    tool_kit: dict[str, Any] = {}
    for tool in import_and_generate_schema(plugin_directory, root_folder):
        print(tool["ns"])
        instance = tool["instance"]
        for method_name, schema in tool["schema"].items():
            tool_kit[method_name] = (instance, schema)
    return tool_kit


def import_and_generate_schema(plugin_directory: str, root_folder: str) -> list[dict[str, Any]]:
    """
    Imports all tools in a plugin directory and generates a JSON schema for each tool.

    Args:
        plugin_directory (str): The directory to search for plugins.
        root_folder (str): The root folder of the workspace.

    Returns:
        list[dict[str, Any]]: The list of schemas.
    """
    schemas = []
    for filename in os.listdir(plugin_directory):
        if filename.endswith("_tool.py"):
            # Construct module name and class name
            module_name = filename[:-3]  # Remove '.py'
            class_name = filename[:-8].capitalize() + "Tool"  # Construct class name

            # Dynamically import module
            module = importlib.import_module(f"plugins.{module_name}")

            # Get class reference
            cls = getattr(module, class_name)

            # Generate JSON schema
            schema = {"ns": module_name, "schema": convert_to_json_schema(cls), "instance": cls(root_folder)}
            schemas.append(schema)
    return schemas


def handle_tool(method_name: str, bots_kwargs: Any, instance: Any) -> Any:
    """
    Handles a tool invocation.

    Args:
        method_name (str): The method name to invoke, as provided by bot.
        bots_kwargs (Any): The arguments to pass to the method as provided by bot.
        instance (Any): The instance to invoke the method on.
    """
    # TODO: handle mime_types
    mime_type = bots_kwargs.get("mime_type")
    if mime_type:
        del bots_kwargs["mime_type"]
    return getattr(instance, method_name)(**bots_kwargs)


if __name__ == "__main__":

    def run() -> None:
        """Example of how to use this module."""
        print(import_and_generate_schema("plugins", "."))
        tool_kit = convert_to_toolkit("plugins", ".")

        # tool callbacks give us a method name, which we lookup in toolkit
        # and
        for method_name, _tool in tool_kit.items():
            instance = tool_kit[method_name][0]
            schema = tool_kit[method_name][1]
            bots_kwargs = generate_data_for_schema(schema)
            result = handle_tool(method_name, bots_kwargs, instance)
            print(f"Invoking... {method_name}() == {result}")

    run()
