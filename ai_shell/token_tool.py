"""
Token Counting.

TODO: Maybe this shouldn't be a bot tool. It should be a utility function.
"""

import tiktoken

from ai_shell.utils.config_manager import Config


class TokenCounterTool:
    """Count the number of tokens in a string."""

    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the FindTool class.

        Args:
            root_folder (str): The root folder path for file operations.
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder
        self.config = config
        model = config.get_value("token_model")
        if not model:
            raise ValueError("token_model must be set in the config")
        self.token_model = model

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a string.

        Args:
            text (str): The text to count the tokens in.

        Returns:
            int: The number of tokens.
        """
        if not text:
            return 0
        # gpt3 turbo - cl100k_base
        # gpt2 (or r50k_base) 	Most GPT-3 models
        # p50k_base 	Code models, text-davinci-002, text-davinci-003
        # cl100k_base 	text-embedding-ada-002
        # enc = tiktoken.get_encoding("cl100k_base")

        encoding = tiktoken.encoding_for_model(self.token_model)
        tokens = encoding.encode(text)
        token_count = len(tokens)
        return token_count
