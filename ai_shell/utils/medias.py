"""
Support various media types without a function for each.
"""
import csv
import io
from typing import Any

import markpickle
import toml
import yaml


def convert_to_media_type(result: dict[str, Any], media_type: str) -> dict[str, str]:
    """
    Converts the given dictionary to a specified media type format.

    Args:
        result: The dictionary to be converted.
        media_type: The desired output format. Supported types are "text/csv", "text/toml", and "text/yaml".

    Returns:
        A string representing the converted dictionary in the specified media type format.

    Raises:
        ValueError: If the specified media type is not supported.
    """
    value = ""
    if media_type == "text/csv":
        value = dict_to_csv(result)
    elif media_type == "text/toml":
        value = toml.dumps(result)
    elif media_type == "text/yaml":
        value = yaml.dump(result)
    elif media_type == "text/markdown":
        config = markpickle.Config()
        config.serialize_dict_as_table = False
        config.serialize_child_dict_as_table = False
        value = markpickle.dumps(result, config=config)
    else:
        raise ValueError("Unsupported media type")
    return {"media_type": media_type, "value": value}


def dict_to_csv(result: dict[str, Any]) -> str:
    """
    Converts a dictionary to a CSV format string.

    Args:
        result: The dictionary to be converted.

    Returns:
        A string representing the dictionary in CSV format.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    for key, value in result.items():
        writer.writerow([key, value])
    return output.getvalue()
