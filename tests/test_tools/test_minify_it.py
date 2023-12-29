from ai_shell.pyutils.minify_it import strip_comments_docstrings, strip_docstrings_with_regex


def test_strip_comments_docstrings():
    # Sample Python code with docstrings for demonstration
    sample_code = """
# I have a comment
def example_function():
    \"""
    # comment
    This is a docstring for example_function.
    \"""
    x = 1 +1
    
    "Yo"

class ExampleClass:
    \"""
    Docstring for ExampleClass.
    \"""
    
    def method(self):
        \"""
        Docstring for method.
        \"""
        yx = 1 +1
    """

    # Applying the function to the sample code
    stripped_code_sample = strip_comments_docstrings(sample_code)
    assert (
        stripped_code_sample
        == """def example_function():
    x = 1 + 1
    \"""Yo\"""


class ExampleClass:

    def method(self):
        yx = 1 + 1
"""
    )


def test_strip_docstrings_with_regex():
    # Sample Python code with docstrings for demonstration
    sample_code_with_regex = """
    def example_function():
        \"""
        This is a docstring for example_function.
        \"""
        pass

    class ExampleClass:
        \"""
        Docstring for ExampleClass.
        \"""

        def method(self):
            \"""
            Docstring for method.
            \"""
            pass
    """

    # Applying the regex-based function to the sample code
    stripped_code_sample_with_regex = strip_docstrings_with_regex(sample_code_with_regex)
    assert (
        stripped_code_sample_with_regex
        == """
    def example_function():
        
        pass

    class ExampleClass:
        

        def method(self):
            
            pass
    """
    )
