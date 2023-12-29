# ai_shell

OpenAI-centric shell for giving safe, chat-optimized, filesystem access to an Assistant as a "tool".

Even if you trust the bot to run bash directly on your machine or docker container, standard tools will run up your
bill with excess tokens in the reply, or a command generates too few tokens and the bot doesn't know what is
going on.

This is an alternative to `code_interpreter`, tools running code in docker container locally, or tools running arbitrary
shell code locally.

## Installation

`pip install ai_shell`

## Usage

See these full examples. As long as the OPENAI_API_KEY environment variable is set, you can run these examples.

- [Pylint bot](https://github.com/matthewdeanmartin/ai_shell/blob/main/ai_shell/demo_bots/pylint_bot.py) will
  attempt to
  fix python
  code lint issues.
- [Test writer bot](https://github.com/matthewdeanmartin/ai_shell/blob/main/ai_shell/demo_bots/test_writer_bot.py) will attempt to
  write unit tests for python code.
- [Tool tester bot](https://github.com/matthewdeanmartin/ai_shell/blob/main/ai_shell/demo_bots/tool_tester_bot.py) tries out tools
  to see if they basically work.

To execute demo bots, run these commands and follow initialization instructions if needed. They all expect to
manipulate python code in an /src/ folder.

```shell
python -m ai_shell.demo_bots.docs_writer_bot
python -m ai_shell.demo_bots.pylint_bot
python -m ai_shell.demo_bots.test_writer_bot
python -m ai_shell.demo_bots.tool_tester_bot
```

This is the python interface to the tools, how you're expected to wire up the tool to your bot.

```python
import ai_shell

cat = ai_shell.CatTool(".")
print(cat.cat(["file.py"]))
print(cat.cat_markdown(["file.py"]))

ls = ai_shell.LsTool(".")
print(ls.ls("docs"))
print(ls.ls_markdown("docs"))
```

This is the smallest example to illustrate basic capabilities, also
see [here](https://github.com/matthewdeanmartin/ai_shell/blob/main/example_tiny_bot.py).

```python
import asyncio
import ai_shell


async def main():
    def static_keep_going(toolkit: ai_shell.ToolKit):
        usage = toolkit.get_tool_usage_for("ls")
        if usage["count"] > 0:
            return (
                "Great job! You've used ls. Summarize in paragraph form and we're done."
            )
        return (
            "You haven't used the ls tool yet. Do you have access to the ls tool? If"
            " there is a problem report it to the report_text tool to end the session."
        )

    # Creates temporary bots
    bot = ai_shell.TaskBot(
        ai_shell.Config(),
        name="Folder inspection bot.",
        bot_instructions="Run the ls tool and tell me what you see.",
        model="gpt-3.5-turbo-1106",
        dialog_logger_md=ai_shell.DialogLoggerWithMarkdown("./tmp"),
    )
    await bot.initialize()
    the_ask = f"""You are in the './' folder. You do not need to guess the pwd, it is './'. 
    Run ls and tell me what you see in paragraph format."""
    await bot.basic_tool_loop(
        the_ask=the_ask,
        root_folder="./src",
        tool_names=[
            "ls",
            "report_text",
        ],
        keep_going_prompt=static_keep_going,
    )


if __name__ == "__main__":
    asyncio.run(main())
```

This is the cli interface, which is intended for testing, not for bot usage.

```shell
ais cat_markdown --file-paths pyproject.toml
```

## Features in Brief

- Many cli-like tools interfaces, such as ls, cat, grep, head, tail, and git.
- OpenAI glue for all cli tools.
- UX with a bot in mind.
- Security with mischievous but not especially malicious bot in mind.
- Bot (Assistant) boilerplate help
- Support for bots doing one shot tool use and goal function driven tool use.
- Bot have extensibility points.
- TODO: plugin system for tools.

## Analogues supported today

**Directories**: ls, find

**Files**: cat, grep, head, tail

**Editing**: sed, ed, edlin, patch, replace, insert, rewrite, write new

**Data**: cut

**Other**: pycat, token counter, git

**Tasking**: todo

## Prior Art

ai_shell draws inspiration from various command-line interface (CLI) tools and shell environments, integrating
features from traditional shells with OpenAI's language models. It is designed to provide an easy and secure interface
for AI-assisted file system interactions, keeping in mind both usability and safety.

## Documentation

- [Features](https://github.com/matthewdeanmartin/ai_shell/blob/main/docs/Features.md)
- [Design](https://github.com/matthewdeanmartin/ai_shell/blob/main/docs/Design.md)
- [Use Cases](https://github.com/matthewdeanmartin/ai_shell/blob/main/docs/Usecases.md)
- [TODO](https://github.com/matthewdeanmartin/ai_shell/blob/main/docs/TODO.md)
- [API docs, pdoc3 style](https://matthewdeanmartin.github.io/ai_shell/)
