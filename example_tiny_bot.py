"""Bot with no extra logging or config."""
import asyncio

from dotenv import load_dotenv

import ai_shell

load_dotenv()

async def main():
    async def static_keep_going(toolkit: ai_shell.ToolKit):
        usage = toolkit.get_tool_usage_for("ls")
        if usage["count"] > 0:
            # Objective completion of goal.
            return "DONE"
            # TODO: Let people thank the bot.
            # " Great job! You've used ls. Summarize in paragraph form and we're done."
        return (
            "You haven't used the ls tool yet. Do you have access to the ls tool? If"
            " there is a problem report it to the report_text tool to end the session."
        )

    # Creates temporary bots
    bot = ai_shell.TaskBot(
        ai_shell.Config(),
        name="Folder inspection bot.",
        bot_instructions="Run the ls tool and tell me what you see.",
        model="gpt-4o-mini",
        dialog_logger_md=ai_shell.DialogLoggerWithMarkdown("./tmp"),
    )
    await bot.initialize()
    the_ask = """You are in the './' folder. You do not need to guess the pwd, it is './'. 
    Run ls and tell me what you see in paragraph format."""
    await bot.basic_tool_loop(
        the_ask=the_ask,
        root_folder="./src",
        tool_names=[
            "ls",
            "report_text",
        ],
        keep_going_prompt=static_keep_going,
        stop_on_no_tool_use=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
