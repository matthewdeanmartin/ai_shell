"""
Support various media types without a function for each.
"""
import csv
import io
import logging
from typing import Any, Union

import toml
import yaml

logger = logging.getLogger(__name__)


def convert_to_media_type(result: dict[str, Any], media_type: str) -> Union[str, dict[str, Any]]:
    """
    Converts the given dictionary to a string that will be returned as a single great big
    string. The bot always gets json, so a json encoded string goes across the wire.

    Args:
        result: The dictionary to be converted.
        media_type: The desired output format. Supported types are "text/csv", "text/toml", and "text/yaml".

    Returns:
        A string representing the converted dictionary in the specified media type format.

    Raises:
        ValueError: If the specified media type is not supported.
    """
    if media_type == "text/csv":
        logger.info("Converting to csv")
        return dict_to_csv(result)
    if media_type == "text/toml":
        logger.info("Converting to toml")
        return toml.dumps(result)
    if media_type == "text/yaml":
        logger.info("Converting to yaml")
        return yaml.dump(result)
    # elif media_type == "text/markdown":
    #     config = markpickle.Config()
    #     config.serialize_dict_as_table = False
    #     config.serialize_child_dict_as_table = False
    #     value = markpickle.dumps(result, config=config)
    logger.warning(f"Unsupported media type: {media_type}")
    return result


def dict_to_csv(result: Union[dict[str, Any], list[str], str]) -> str:
    """
    Converts a dictionary to a CSV format string.

    Args:
        result: The dictionary to be converted.

    Returns:
        A string representing the dictionary in CSV format.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    if isinstance(result, dict):
        for key, value in result.items():
            writer.writerow([key, value])
    if isinstance(result, list):
        for item in result:
            writer.writerow([item])
    if isinstance(result, str):
        writer.writerow([result])
    return output.getvalue()
