import tokenize


def find_function_code(file_path, function_name):
    """
    Finds the start and end lines of a function in a Python file.

    Args:
        file_path (str): Path to the Python file.
        function_name (str): Name of the function to find.

    Returns:
        tuple: A tuple containing the file name, function name, and a range of line numbers, or None if not found.
    """
    with open(file_path, encoding="utf-8") as file:
        tokens = tokenize.generate_tokens(file.readline)
        function_line = None
        depth = 0

        for token in tokens:
            token_type, token_string, start, _, _ = token

            if function_line is not None:
                if token_type == tokenize.INDENT:
                    depth += 1
                elif token_type == tokenize.DEDENT:
                    depth -= 1

                if depth == 0:
                    end_line = start[0] - 1
                    return file_path, function_name, (function_line, end_line)

            if token_type == tokenize.NAME and token_string == "def" and depth == 0:
                next_token, _ = next(tokens), next(tokens)  # Skip 'def' and get the function name
                if next_token.string == function_name:
                    function_line = start[0]

    return None  # Function not found


if __name__ == "__main__":
    # Example usage
    file_name, func_name, lines = find_function_code("source_refs.py", "find_function_code")
    if lines:
        print(f"File: {file_name}, Function: {func_name}, Lines: {lines}")
    else:
        print("Function not found.")
