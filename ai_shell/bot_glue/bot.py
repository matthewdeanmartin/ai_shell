"""
Simple bot that doesn't need any tools
"""
from openai.types.beta.threads.run_create_params import (
    ToolAssistantToolsCode,
    ToolAssistantToolsFunction,
    ToolAssistantToolsRetrieval,
)
from openai.types.shared_params import FunctionDefinition

# pylint: disable=wrong-import-position, using-constant-test
if True:
    import openai_multi_tool_use_parallel_patch

import logging.config
from collections.abc import Awaitable, Callable
from typing import Any, Optional, cast

import openai
from openai.types.beta import Assistant, Thread

from ai_shell.bot_glue.tool_utils import loop_tools
from ai_shell.openai_toolkit import ToolKit
from ai_shell.openai_tools import ALL_TOOLS, initialize_all_tools
from ai_shell.utils.config_manager import Config
from ai_shell.utils.log_conversation import DialogLoggerWithMarkdown

logger = logging.getLogger(__name__)

# Adding line so module isn't unused
if not openai_multi_tool_use_parallel_patch:
    print("Adding code so pylint doesn't think the module is unused.")


class TaskBot:
    """Minimal bot management code."""

    def __init__(
        self,
        config: Config,
        name: str,
        bot_instructions: str,
        model: str,
        dialog_logger_md: DialogLoggerWithMarkdown,
        persist_bots: bool = False,
        persist_threads: bool = False,
        maximum_loops: int = 10,
    ):
        self.model = model
        """Model, name and instructions uniquely identify a bot."""
        self.name = name
        """Model, name and instructions uniquely identify a bot."""
        self.bot_instructions = bot_instructions
        """Model, name and instructions uniquely identify a bot."""

        self.client: openai.AsyncOpenAI = openai.AsyncOpenAI()
        self.thread: Optional[Thread] = None
        self.assistant: Optional[Assistant] = None

        self.dialog_logger_md = dialog_logger_md
        """Conversation style logger"""

        self.persist_bots = persist_bots
        """Keep bots or attempt to delete them at end of session"""

        self.persist_threads = persist_threads
        """Keep thread or attempt to delete them"""

        self.config = config
        """Stores bot, thread config and other global config."""

        self.maximum_loops = maximum_loops
        """Prevent infinite loops and money wastage."""

        self.toolkit: Optional[ToolKit] = None
        """Reference to toolkit so that goal checkers can check if any tools were used."""

        self.allow_self_certification = False
        """Do you want to trust the bot when it says it has achieved the goal?"""

    async def initialize(self) -> None:
        """Get or create a bot and store it in the config."""
        bot = await self.get_create_bot()
        logger.debug(f"Assistant id: {bot.id}")
        self.assistant = bot
        self.dialog_logger_md.write_header(bot_name=self.name, model=self.model, bot_instructions=self.bot_instructions)

    async def get_create_bot(self) -> Assistant:
        """Get or create a bot and store it in the config."""
        current_bot = self.config.get_bot(self.name)
        if not current_bot:
            await self.create_bot()
        else:
            try:
                self.assistant = await self.client.beta.assistants.retrieve(current_bot.assistant_id)
                logger.debug(f"Assistant retrieved: {self.assistant.id}")
            except openai.NotFoundError:
                await self.create_bot()
        if not self.assistant:
            raise TypeError("Assistant not found or created.")
        logger.debug(f"Assistant id: {self.assistant.id}")
        return self.assistant

    async def create_bot(self):
        """Create a bot and store it in the config."""
        self.assistant = await self.client.beta.assistants.create(
            name=self.name,
            instructions=self.bot_instructions,
            model=self.model,
        )
        self.config.add_bot(self.assistant.id, self.name)
        logger.debug(f"Assistant created: {self.assistant.id}")

    def toolkit_factory(
        self, root_folder: str, model: str, tool_names: list[str]
    ) -> tuple[ToolKit, list[ToolAssistantToolsCode | ToolAssistantToolsRetrieval | ToolAssistantToolsFunction]]:
        self.toolkit = ToolKit(root_folder, model, 500, permitted_tools=tool_names, config=self.config)
        initialize_all_tools(keeps=tool_names)
        tools_schema: list[ToolAssistantToolsCode | ToolAssistantToolsRetrieval | ToolAssistantToolsFunction] = [
            ToolAssistantToolsFunction(**{"function": cast(FunctionDefinition, schema), "type": "function"})
            for schema in ALL_TOOLS
        ]
        if not tools_schema:
            raise Exception("Not enough tools!")
        return self.toolkit, tools_schema

    async def one_shot_ask(self, the_ask: str) -> Any:
        """Free-form request, structured response.

        Args:
            the_ask (str): The request.

        Returns:
            Any: The response.
        """
        if not self.toolkit:
            raise TypeError("Missing toolkit before one_shot_ask")
        if not self.assistant:
            raise TypeError("Missing assistant before one_shot_ask")
        try:
            _, tool_schemas = self.toolkit_factory(
                ".",
                self.model,
                [
                    # "report_bool",
                    "report_dict",
                    "report_float",
                    "report_int",
                    # "report_json",
                    "report_list",
                    # "report_set",
                    # "report_text", Why? Just do an unstructured query.
                    # "report_toml",
                    # "report_tuple",
                    # "report_xml",
                ],
            )
            thread = await self.client.beta.threads.create()
            logger.info(the_ask)
            _message = await self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=the_ask,
            )
            # pydantic_tools =[run_create_params.Tool(_) for _ in tool_schemas]
            run = await self.client.beta.threads.runs.create(
                thread_id=thread.id, assistant_id=self.assistant.id, tools=tool_schemas
            )
            tool_use_count = await loop_tools(self.client, self.toolkit, run, thread, self.dialog_logger_md)
            if tool_use_count == 0:
                logger.warning("No tool usage, something went wrong.")

            messages = await self.client.beta.threads.messages.list(thread_id=thread.id, order="desc")
            # logger.info(messages)
            last_words = parse_message(messages)
            logger.info(last_words)
            self.dialog_logger_md.add_bot(last_words)

        except Exception as exception:
            self.dialog_logger_md.add_error(exception)
            raise
        finally:
            # clean up thread
            if self.thread and not self.persist_threads:
                await self.client.beta.threads.delete(self.thread.id)
            if self.assistant and not self.persist_bots:
                # clean up assistant
                await self.client.beta.assistants.delete(self.assistant.id)

    async def basic_tool_loop(
        self,
        the_ask: str,
        root_folder: str,
        tool_names: list[Any],
        keep_going_prompt: Callable[[ToolKit], Awaitable[str]],
    ) -> None:
        """
        Loop through tool requests.

        Args:
            the_ask (str): The initial request.
            root_folder (str): The root folder for file operations.
            tool_names (list[Any]): The tools to use.
            keep_going_prompt (str): The prompt to use to keep going.

        Returns:
            None
        """
        if not self.assistant:
            raise TypeError("Missing assistant before basic_tool_loop")

        if self.dialog_logger_md:
            self.dialog_logger_md.add_user(the_ask)
            self.dialog_logger_md.add_toolkit(tool_names)

        tool_loops = 0
        total_tool_use_count = 0
        try:
            tool_names.append("report_text")
            tool_names = list(set(tool_names))
            _, tool_schemas = self.toolkit_factory(root_folder, self.model, tool_names)
            if not self.toolkit:
                raise TypeError("Missing toolkit before basic_tool_loop")
            thread = await self.client.beta.threads.create()
            logger.info(the_ask)
            _message = await self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=the_ask,
            )
            run = await self.client.beta.threads.runs.create(
                thread_id=thread.id, assistant_id=self.assistant.id, tools=tool_schemas
            )
            tools_used_this_round = await loop_tools(self.client, self.toolkit, run, thread, self.dialog_logger_md)
            tool_loops += 1
            if tool_loops > self.maximum_loops:
                raise TypeError("Too many tool loops")

            total_tool_use_count += tools_used_this_round

            messages = await self.client.beta.threads.messages.list(thread_id=thread.id, order="desc")
            initial_bot_response = parse_message(messages)
            self.dialog_logger_md.add_bot(initial_bot_response)

            # Did you use any tools?
            if tools_used_this_round == 0:
                initial_user_response = (
                    "I see you didn't use any tools.  "
                    "Please list what tools you have available, and if there are some available, "
                    "why they were not useful."
                )
            else:
                if not self.toolkit:
                    raise TypeError("Missing toolkit before keep_going_prompt")
                initial_user_response = await keep_going_prompt(self.toolkit)

            # TODO: make into method.
            await self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=initial_user_response,
            )
            run = await self.client.beta.threads.runs.create(thread_id=thread.id, assistant_id=self.assistant.id)
            self.dialog_logger_md.add_user(initial_user_response)

            # "keep going/done" loop
            done = "NOPE"
            tools_used_this_round = -1

            # TODO: intializee this in constructor
            if hasattr(self.toolkit, "tool_answer_collector") and self.toolkit.tool_answer_collector:
                final_report = self.toolkit.tool_answer_collector.text_answer
                final_comment = self.toolkit.tool_answer_collector.comment
                self.dialog_logger_md.add_bot(f"Final word: {final_report}, {final_comment}")
                return

            # Bot has at least 3 ways to stop
            # - return message of DONE
            # - use answer tool to submit DONE, or IMPOSSIBLE
            # - stop using tools
            while done != "DONE" or tools_used_this_round == 0:
                tools_used_this_round = await loop_tools(self.client, self.toolkit, run, thread, self.dialog_logger_md)
                # Did we use any tools
                total_tool_use_count += tools_used_this_round

                # infinite loop protection
                tool_loops += 1
                if tool_loops > self.maximum_loops:
                    raise TypeError("Too many tool loops")

                messages = await self.client.beta.threads.messages.list(thread_id=thread.id, order="desc")
                successive_response = parse_message(messages)
                self.dialog_logger_md.add_bot(successive_response)
                done = capture_done_message(messages)
                if done == "DONE":
                    break

                # Did bot use tool to submit final report. Wow. Can't trust all bots.
                if (
                    self.allow_self_certification
                    and hasattr(self.toolkit, "tool_answer_collector")
                    and self.toolkit.tool_answer_collector
                ):
                    final_report = str(self.toolkit.tool_answer_collector.text_answer).upper().strip()
                    final_comment = self.toolkit.tool_answer_collector.comment
                    self.dialog_logger_md.add_bot(f"Final word: {final_report}, {final_comment}")
                    break

                if done != "DONE":
                    # Replace with 2nd bot?
                    keep_going_text = await keep_going_prompt(self.toolkit)
                    if keep_going_text == "DONE":
                        # The bot did a good job and we can certify that.
                        break
                    self.dialog_logger_md.add_user(keep_going_text)
                    logger.info(keep_going_text)
                    await self.client.beta.threads.messages.create(
                        thread_id=thread.id,
                        role="user",
                        content=keep_going_text,
                    )
                    run = await self.client.beta.threads.runs.create(
                        thread_id=thread.id, assistant_id=self.assistant.id
                    )

        except Exception as exception:
            self.dialog_logger_md.add_error(exception)
            raise
        finally:
            # clean up thread
            if self.thread and not self.persist_threads:
                await self.client.beta.threads.delete(self.thread.id)
            if self.assistant and not self.persist_bots:
                # clean up assistant
                await self.client.beta.assistants.delete(self.assistant.id)


def parse_message(messages) -> str:
    """Return the last message in messages"""
    for key, message in messages:
        if key == "data":
            text_message = message[0].content[0].text.value
            return text_message
    raise TypeError("Couldn't find data/message/content")


def capture_done_message(messages) -> str:
    """Return DONE if found in messages"""
    # Replace with structured?
    done = ""
    for key, message in messages:
        if key == "data":
            text_message = message[0].content[0].text.value
            if "DONE" in str(text_message).upper():
                done = "DONE"
                break
    return done
