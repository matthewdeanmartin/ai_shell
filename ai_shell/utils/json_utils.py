"""
Tools for handling AI's peculiar way of making json
"""
import dataclasses
import datetime
import http
import json as slowjson
import logging
import sys
import types
from typing import Any

import orjson
import untruncate_json

logger = logging.getLogger(__name__)


class FatalConfigurationError(Exception):
    """A fatal configuration error."""


def loosy_goosy_default_encoder(o: Any) -> Any:
    """Tell json how to serialize basic things
    # https://stackoverflow.com/a/8230505/33264
    """
    # if isinstance(o, set):
    #     return list(o)
    if isinstance(o, types.GeneratorType):
        return list(o)
    # if dataclasses.is_dataclass(o):
    #     return dataclasses.asdict(o)
    # if isinstance(o, datetime.datetime):
    #     return o.isoformat()
    raise TypeError("orjson can't handle this.")


class LoosyGoosyEncoderForSlowJson(slowjson.JSONEncoder):
    """Encode what json will not.
    # https://stackoverflow.com/a/8230505/33264
    """

    def default(self, o):
        """Tell json how to serialize basic things"""
        if isinstance(o, set):
            return list(o)
        if isinstance(o, types.GeneratorType):
            return list(o)
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return slowjson.JSONEncoder.default(self, o)


def try_everything(args_text: str) -> Any:
    """Try to parse json, untruncate, and double escape"""
    success = False
    attempted: set[str] = set()
    current_error = None
    loop_count = 0
    while not success and len(attempted) < 3 and loop_count < 10:
        # looking for infinite loop
        loop_count += 1
        try:
            arguments = orjson.loads(args_text)
            return arguments
        except orjson.JSONDecodeError as error:
            logger.error(error)
            if not attempted:
                # first fall back
                args_text = untruncate_json.complete(args_text)
                attempted.add("untruncate")
            elif "\\" in args_text:
                args_text = args_text.replace("\\", "\\\\")
                attempted.add("double escape")
            elif "Expecting property name enclosed in double quotes" in error.msg:
                # json library (slow one)
                args_text = args_text.replace("'", '"')
                attempted.add("single to double quotes")
            elif "unexpected character" in error.msg and "'" in args_text:
                # orjson
                args_text = args_text.replace("'", '"')
                attempted.add("single to double quotes")
            current_error = error
    if loop_count >= 10:
        raise RuntimeError(f"Infinite loop detected: {args_text}, {current_error}")
    if current_error:
        raise current_error


def exception_to_rfc7807_dict(exception: Exception) -> dict[str, Any]:
    """
    Convert an exception to a dictionary conforming to RFC 7807.

    Args:
        exception (Exception): The exception to convert.

    Returns:
        dict[str, Any]: A dictionary structured according to RFC 7807.

    The function maps common Python standard library exceptions to HTTP status codes.
    If an exception is not in the predefined mapping, the status code defaults to 500 (Internal Server Error).
    """
    if isinstance(exception, FatalConfigurationError):
        logger.error(exception)
        print("FatalConfigurationError: " + str(exception))
        sys.exit(1)

    # Mapping of standard exceptions to HTTP status codes and documentation URLs
    exception_mapping = {
        ValueError: (http.HTTPStatus.BAD_REQUEST, "https://docs.python.org/3/library/exceptions.html#ValueError"),
        PermissionError: (
            http.HTTPStatus.FORBIDDEN,
            "https://docs.python.org/3/library/exceptions.html#PermissionError",
        ),
        FileNotFoundError: (
            http.HTTPStatus.NOT_FOUND,
            "https://docs.python.org/3/library/exceptions.html#FileNotFoundError",
        ),
        KeyError: (http.HTTPStatus.NOT_FOUND, "https://docs.python.org/3/library/exceptions.html#KeyError"),
        TimeoutError: (
            http.HTTPStatus.REQUEST_TIMEOUT,
            "https://docs.python.org/3/library/exceptions.html#TimeoutError",
        ),
        NotImplementedError: (
            http.HTTPStatus.NOT_IMPLEMENTED,
            "https://docs.python.org/3/library/exceptions.html#NotImplementedError",
        ),
    }

    # Get the corresponding status code and documentation URL or default to 500 Internal Server Error and None
    status_code, doc_url = exception_mapping.get(exception.__class__, (http.HTTPStatus.INTERNAL_SERVER_ERROR, None))

    # Construct the error dictionary
    error_dict = {
        "type": doc_url,
        "title": exception.__class__.__name__,
        "status": status_code.value,
        "detail": str(exception) if str(exception) else None,
    }
    for key in list(error_dict.keys()):
        if error_dict[key] is None:
            del error_dict[key]
    return error_dict
