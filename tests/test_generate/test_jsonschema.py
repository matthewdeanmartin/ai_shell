from jsonschema.validators import Draft7Validator

from ai_shell.code_generate.method_to_jsonschema import convert_to_json_schema, extract_class_methods_details


def test_simple():
    # Example usage with a modified sample class
    class SampleClass:
        def method1(self, arg1: int, arg2: str = "default") -> bool:
            """Method1

            Args:
                arg1 (int): Description for arg1.
                arg2 (str): Description for arg2.

            Returns:
                bool: Description for return value.
            """

        def method2(self, arg3, arg4: float = 3.14) -> bool:
            """Method2

            Args:
                arg3: Description for arg3.
                arg4 (float): Description for arg4.

            Returns:
                bool: Description for return value.
            """
            return True

    # methods_info = extract_class_methods_details(SampleClass)
    # Converting to JSON schema
    json_schema = convert_to_json_schema(SampleClass)
    assert json_schema
    for _function_name, schema in json_schema.items():
        Draft7Validator.check_schema(schema)
    # Display the JSON schema in a readable format
    # print(json.dumps(json_schema, indent=4))


def test_with_docstring():
    # Example usage
    class SampleClass:
        def method1(self, arg1: int, arg2: str = "default"):
            """
            Short description for method1.

            Args:
                arg1 (int): Description for arg1.
                arg2 (str): Description for arg2.
            """

        def method2(self, arg3, arg4: float = 3.14) -> bool:
            """
            Short description for method2.

            Args:
                arg3: Description for arg3.
                arg4 (float): Description for arg4.
            """
            return True

    # Convert to JSON schema with descriptions
    json_schema_with_descriptions = convert_to_json_schema(SampleClass)
    for _function_name, schema in json_schema_with_descriptions.items():
        Draft7Validator.check_schema(schema)
    # Display the JSON schema in a readable format
    # print(json.dumps(json_schema_with_descriptions, indent=4))


class TestClassForMethodInfo:
    def method1(self, param1: int, param2: str = "default"):
        """A test method"""

    def method2(self, param3: bool) -> float:
        """Another test method"""
        return 3.14


def test_extract_class_methods_details():
    expected_output = {
        "method1": {
            "args": [("self", None, None), ("param1", int, None), ("param2", str, "default")],
            "return_type": None,
        },
        "method2": {"args": [("self", None, None), ("param3", bool, None)], "return_type": float},
    }

    actual_output = extract_class_methods_details(TestClassForMethodInfo)
    # Why is this here?!
    cloned_actual_output = actual_output.copy()
    if "__pytest_asyncio_scoped_event_loop" in actual_output:
        del cloned_actual_output["__pytest_asyncio_scoped_event_loop"]
    assert cloned_actual_output == expected_output, "Method details extraction does not match expected output."
