"""
Simple bot that doesn't need any toolkit_factory
"""
import logging.config
from typing import Any, Optional

import openai
import openai_multi_tool_use_parallel_patch
from openai.types.beta import Assistant

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

        self.client = openai.AsyncOpenAI()
        self.thread = None
        self.assistant = None

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

    async def initialize(self):
        bot = await self.get_create_bot()
        logger.debug(f"Assistant id: {bot.id}")
        self.assistant = bot
        self.dialog_logger_md.write_header(bot_name=self.name, model=self.model, bot_instructions=self.bot_instructions)

    async def get_create_bot(self) -> Assistant:
        current_bot = self.config.get_bot(self.name)
        if not current_bot:
            assistant = await self.client.beta.assistants.create(
                name=self.name,
                instructions=self.bot_instructions,
                model=self.model,
                # no toolkit_factory
            )
            self.config.add_bot(self.assistant.id, self.name)
            logger.debug(f"Assistant created: {assistant.id}")
        else:
            assistant = await self.client.beta.assistants.retrieve(current_bot.assistant_id)
            logger.debug(f"Assistant retrieved: {assistant.id}")
        logger.debug(f"Assistant id: {assistant.id}")
        return assistant

    def toolkit_factory(
        self, root_folder: str, model: str, tool_names: list[str]
    ) -> tuple[ToolKit, list[dict[str, Any]]]:
        self.toolkit = ToolKit(root_folder, model, 500, permitted_tools=tool_names)
        initialize_all_tools(keeps=tool_names)
        tools_schema = [{"function": schema, "type": "function"} for schema in ALL_TOOLS]
        if not tools_schema:
            raise Exception("Not enough toolkit_factory!")
        return self.toolkit, tools_schema

    async def one_shot_ask(self, the_ask: str) -> Any:
        """Free-form request, structured response."""
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
        self, the_ask: str, root_folder: str, tool_names: list[Any], keep_going_prompt: str
    ) -> Any:
        """Work flow:

        - ask for something
        - let bot loop through tool usage
        - Ask bot if they are done (static message, bot decides)
        - Loop until they say they are done.
        """
        if self.dialog_logger_md:
            self.dialog_logger_md.add_user(the_ask)
            self.dialog_logger_md.add_toolkit(tool_names)

        tool_loops = 0
        total_tool_use_count = 0
        try:
            tool_names.append("report_text")
            tool_names = list(set(tool_names))
            _, tool_schemas = self.toolkit_factory(root_folder, self.model, tool_names)
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

            # Did you use any toolkit_factory?
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
                final_report = str(self.toolkit.tool_answer_collector.text_answer).upper().strip()
                final_comment = self.toolkit.tool_answer_collector.comment
                self.dialog_logger_md.add_bot(f"Final word: {final_report}, {final_comment}")
                return

            # Bot has at least 3 ways to stop
            # - return message of DONE
            # - use answer tool to submit DONE, or IMPOSSIBLE
            # - stop using toolkit_factory
            while done != "DONE" or tools_used_this_round == 0:
                tools_used_this_round = await loop_tools(self.client, self.toolkit, run, thread, self.dialog_logger_md)
                # Did we use any toolkit_factory
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

                # Did bot use tool to submit final report
                if hasattr(self.toolkit, "tool_answer_collector") and self.toolkit.tool_answer_collector:
                    final_report = str(self.toolkit.tool_answer_collector.text_answer).upper().strip()
                    final_comment = self.toolkit.tool_answer_collector.comment
                    self.dialog_logger_md.add_bot(f"Final word: {final_report}, {final_comment}")
                    break
                if done != "DONE":
                    # Replace with 2nd bot?
                    keep_going_text = await keep_going_prompt(self.toolkit)
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
    for key, message in messages:
        if key == "data":
            text_message = message[0].content[0].text.value
            return text_message
    raise TypeError("Couldn't find data/message/content")


def capture_done_message(messages) -> str:
    # Replace with structured?
    done = ""
    for key, message in messages:
        if key == "data":
            text_message = message[0].content[0].text.value
            if "DONE" in str(text_message).upper():
                done = "DONE"
                break
    return done
