"""
Token Counting
"""

import tiktoken


class TokenCounterTool:
    def __init__(self, root_folder: str) -> None:
        self.root_folder = root_folder
        self.token_model = "gpt-3.5-turbo"  # nosec: This is not a password.

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a string.

        Args:
            text (str): The text to count the tokens in.

        Returns:
            int: The number of tokens.
        """
        # gpt3 turbo - cl100k_base
        # gpt2 (or r50k_base) 	Most GPT-3 models
        # p50k_base 	Code models, text-davinci-002, text-davinci-003
        # cl100k_base 	text-embedding-ada-002
        # enc = tiktoken.get_encoding("cl100k_base")

        encoding = tiktoken.encoding_for_model(self.token_model)
        tokens = encoding.encode(text)
        token_count = len(tokens)
        return token_count
