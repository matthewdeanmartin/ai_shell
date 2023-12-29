"""
Utility for generating jsonschema from class methods.
"""
import inspect
import typing
from typing import Any

from docstring_parser import parse
from jsonschema.validators import Draft7Validator


def extract_class_methods_details(cls):
    """
    Extracts methods, their arguments, default values, and return types from a given class.

    Args:
    cls (class): The class from which to extract methods, arguments, and return types.

    Returns:
    dict: A dictionary where keys are method names and values are dictionaries containing
          'args' (list of tuples with argument name, type, and default value) and 'return_type'.
    """
    methods_info = {}

    # Iterating over all members of the class
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        # Extracting the signature of the method
        sig = inspect.signature(method)
        args_info = []

        # Iterating over all parameters in the method signature
        for param in sig.parameters.values():
            # Extracting name, annotation, and default value of the parameter
            arg_name = param.name
            arg_type = param.annotation if param.annotation is not inspect.Parameter.empty else None
            default_value = param.default if param.default is not inspect.Parameter.empty else None
            args_info.append((arg_name, arg_type, default_value))

        # Extracting return type of the method
        return_type = sig.return_annotation if sig.return_annotation is not inspect.Signature.empty else None

        methods_info[name] = {"args": args_info, "return_type": return_type}

    return methods_info


def convert_to_json_schema(cls) -> dict[str, Any]:
    """
    Converts the extracted class methods information into JSON schema format with descriptions
    from the docstrings.

    Args:
    cls (class): The class from which to extract methods, arguments, and return types.

    Returns:
    dict: A dictionary where keys are method names and values are their corresponding JSON schemas.
    """
    require_descriptions = True
    methods_info = extract_class_methods_details(cls)
    json_schemas = {}

    # Type mapping from Python types to JSON schema types
    type_mapping = {
        int: "integer",
        float: "number",
        str: "string",
        bool: "boolean",
        None: "null",
        list: "array",
        set: "array",
        tuple: "array",
        list[str]: "string",  # TODO how to express this?
        list[str]: "string",
        typing.Optional[int]: ["integer", "null"],  # will nullable types work?
        typing.Optional[str]: ["string", "null"],
        dict[str, typing.Any]: ["object"],
    }

    for method_name, details in methods_info.items():
        # special dunder methods
        if method_name.startswith("__"):
            continue
        # private by convention
        if method_name.startswith("_"):
            continue

        # Parse docstring of the method
        method = getattr(cls, method_name)
        docstring = parse(method.__doc__) if method.__doc__ else None

        schema = {
            "type": "object",
            "properties": {
                "mime_type": {
                    "type": "string",
                    "description": "Return value as text/csv, text/markdown, or text/yaml inside the JSON.",
                }
            },
            "required": [],
        }

        description = ""
        # Add short description if available
        if docstring and docstring.short_description:
            description = docstring.short_description
        else:
            raise TypeError(f"Missing docstring! {method_name}")

        if docstring and docstring.examples:
            for example in docstring.examples:
                if example.description:
                    description += "\n\nExample:\n\n" + example.description

        if require_descriptions and not description:
            raise TypeError(f"Missing description : {method_name}")
        else:
            schema["description"] = description

        for arg_name, arg_type, default in details["args"]:
            # Skipping 'self' argument
            if arg_name == "self":
                continue

            # Mapping Python type to JSON schema type
            json_type = type_mapping.get(arg_type)
            if json_type is None:
                raise ValueError(f"Missing {arg_type} mapping")

            # Adding property to schema
            prop = {
                "type": json_type,
            }
            if default is not None:
                prop["default"] = default

            # Add description from docstring
            if docstring:
                param_desc = next((param.description for param in docstring.params if param.arg_name == arg_name), None)
                if param_desc:
                    prop["description"] = param_desc

            if require_descriptions and not prop.get("description"):
                raise TypeError(f"Missing description {method_name}.{arg_name}")

            # need strongly typed dicts, I guess.
            typing.cast(dict[str, dict[str, typing.Sequence]], schema["properties"])[arg_name] = prop

            # Adding to required list if there's no default value
            if default is None:
                # need strongly typed dicts, I guess.
                typing.cast(list[str], schema["required"]).append(arg_name)

        json_schemas[method_name] = schema

    for _function_name, schema in json_schemas.items():
        Draft7Validator.check_schema(schema)
    return json_schemas
