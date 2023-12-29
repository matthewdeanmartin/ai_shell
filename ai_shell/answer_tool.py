"""
Call a tool, but actually the tool is just a way to get a structured response.

Work flow:
- Ask bot free form question
- Get back an answer in a parsable format.

How is this different from a tool call?
- Tool calls are because the bot wants to know something
- Tool calls args are likely info we gave the bot in the initial prompt
- Tool body does significant work. Here the body just collects the args.


"""
from typing import Any, Optional

from ai_shell.utils.config_manager import Config
from ai_shell.utils.logging_utils import log


class AnswerCollectorTool:
    def __init__(self, root_folder: str, config: Config) -> None:
        """
        Initialize the PytestTool class.

        Args:
            root_folder (str): The root folder path for file operations. (Not used yet)
            config (Config): The developer input that bot shouldn't set.
        """
        self.root_folder = root_folder
        self.config = config
        self.comment: Optional[str] = None
        self.bool_answer: Optional[bool] = None
        self.json_answer: Optional[str] = None
        self.xml_answer: Optional[str] = None
        self.toml_answer: Optional[str] = None
        self.tuple_answer: Optional[tuple] = None
        self.set_answer: Optional[set] = None
        self.text_answer: Optional[str] = None
        self.list_answer: Optional[list[str]] = None
        self.int_answer: Optional[int] = None
        self.float_answer: Optional[float] = None
        self.dict_answer: Optional[dict[str, Any]] = None
        self.response_received = "Response received."

    def _answered(self) -> None:
        """Check if this tool has been used.

        Raises:
            TypeError: If the tool has been used. Recreate a new one after each usage.
        """
        if any(
            [
                self.comment,
                self.bool_answer is not None,
                self.json_answer,
                self.xml_answer,
                self.toml_answer,
                self.tuple_answer,
                self.set_answer,
                self.text_answer,
                self.list_answer,
                self.int_answer,
                self.float_answer,
                self.dict_answer,
            ]
        ):
            raise TypeError("This Answer tool has been used. Please create a new one for another answer.")

    @log()
    def report_list(self, answer: list[str], comment: str = "") -> str:
        """Report answer in list format.

        Args:
            answer (list[str]): The answer to be reported in list format.
            comment (str): Any comments, supplemental info about the answer.

        Returns:
            str: A string indicating that the response has been received.
        """
        self._answered()
        self.list_answer = answer
        self.comment = comment
        return self.response_received

    @log()
    def report_int(self, answer: int, comment: str = "") -> str:
        """Report answer in integer format
        Args:
            answer (int): The answer to be reported in integer format.
            comment (str): Any comments, supplemental info about the answer.


        Returns:
            str: A string indicating that the response has been received.
        """
        self._answered()
        self.int_answer = answer
        self.comment = comment
        return self.response_received

    @log()
    def report_float(self, answer: float, comment: str = "") -> str:
        """Report answer in string format.

        Args:
            answer (float): The answer to be reported in float format.
            comment (str): Any comments, supplemental info about the answer.

        Returns:
            str: A string indicating that the response has been received.
        """
        self._answered()
        self.float_answer = answer
        self.comment = comment
        return self.response_received

    @log()
    def report_dict(self, answer: dict[str, Any], comment: str = "") -> str:
        """Report answer in dict format.

        Args:
            answer (dict[str, Any]): The answer to be reported in dict format.
            comment (str): Any comments, supplemental info about the answer.

        Returns:
            str: A string indicating that the response has been received.
        """
        self._answered()
        self.dict_answer = answer
        self.comment = comment
        return self.response_received

    @log()
    def report_text(self, answer: str, comment: str = "") -> str:
        """Report answer in string format.

        Args:
            answer (str): The answer to be reported in string format.
            comment (str): Any comments, supplemental info about the answer.

        Returns:
            str: A string indicating that the response has been received.
        """
        self._answered()
        self.text_answer = answer
        self.comment = comment
        return self.response_received

    @log()
    def report_bool(self, answer: bool, comment: str = "") -> str:
        """Report answer in bool format.

        Args:
            answer (bool): The answer to be reported in bool format.
            comment (str): Any comments, supplemental info about the answer.

        Returns:
            str: A string indicating that the response has been received.
        """
        self._answered()
        self.bool_answer = answer
        self.comment = comment
        return self.response_received

    @log()
    def report_tuple(self, answer: tuple, comment: str = "") -> str:
        """Report answer in tuple format.

        Args:
            answer (tuple): The answer to be reported in tuple format.
            comment (str): Any comments, supplemental info about the answer.

        Returns:
            str: A string indicating that the response has been received.
        """
        self._answered()
        self.tuple_answer = answer
        self.comment = comment
        return self.response_received

    @log()
    def report_set(self, answer: set, comment: str = "") -> str:
        """Report answer in set format.

        Args:
            answer (set): The answer to be reported in set format.
            comment (str): Any comments, supplemental info about the answer.

        Returns:
            str: A string indicating that the response has been received.
        """
        self._answered()
        self.set_answer = answer
        self.comment = comment
        return self.response_received

    @log()
    def report_json(self, answer: str, comment: str = "") -> str:
        """Report answer in json format.

        Args:
            answer (str): The answer to be reported in json format.
            comment (str): Any comments, supplemental info about the answer.

        Returns:
            str: A string indicating that the response has been received.
        """
        self._answered()
        self.json_answer = answer
        self.comment = comment
        return self.response_received

    @log()
    def report_xml(self, answer: str, comment: str = "") -> str:
        """Report answer in xml format.

        Args:
            answer (str): The answer to be reported in xml format.
            comment (str): Any comments, supplemental info about the answer.

        Returns:
            str: A string indicating that the response has been received.
        """
        self._answered()
        self.xml_answer = answer
        self.comment = comment
        return self.response_received

    @log()
    def report_toml(self, answer: str, comment: str = "") -> str:
        """Report answer in toml format.

        Args:
            answer (str): The answer to be reported in toml format.
            comment (str): Any comments, supplemental info about the answer.

        Returns:
            str: A string indicating that the response has been received.
        """
        self._answered()
        self.toml_answer = answer
        self.comment = comment
        return self.response_received
