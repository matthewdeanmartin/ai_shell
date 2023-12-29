"""
Tools for handling AI's peculiar way of making json
"""
import dataclasses
import datetime
import http
import json
import types
from typing import Any

import untruncate_json

# TODO: Use orjson because it is faster.


class FatalConfigurationError(Exception):
    """A fatal configuration error."""


class LoosyGoosyEncoder(json.JSONEncoder):
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
        return json.JSONEncoder.default(self, o)


def try_everything(args_text: str) -> Any:
    """Try to parse json, untruncate, and double escape"""
    success = False
    attempted: set[str] = set()
    current_error = None
    while not success and len(attempted) < 3:
        try:
            arguments = json.loads(args_text)
            return arguments
        except json.decoder.JSONDecodeError as error:
            if not attempted:
                # first fall back
                args_text = untruncate_json.complete(args_text)
                attempted.add("untruncate")
            elif "\\" in args_text:
                args_text = args_text.replace("\\", "\\\\")
                attempted.add("double escape")
            current_error = error
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
        print("FatalConfigurationError: " + str(exception))
        exit(1)

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
