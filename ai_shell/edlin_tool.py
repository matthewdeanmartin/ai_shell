"""
Give bot access to an edlin clone.

The bot knows edlin, but edlin wasn't originally for headless, batched mode and the DSL for that is somewhat
invented. The bot has a hard time with that part.

The bot has a hard time with quotes, sometimes including them, sometimes not.

It sometimes falls back to "ed" or "vi" conventions.

Also, the edlin clone as of early 2024 still has bugs.
"""
import logging
import logging.config
import traceback

import dedlin
from ai_shell.cat_tool import CatTool
from ai_shell.utils.logging_utils import log
from ai_shell.utils.read_fs import sanitize_path
from dedlin.command_sources import StringCommandGenerator


logger = logging.getLogger(__name__)

VERBOSE = True


class EdlinTool:
    def __init__(self, root_folder: str):
        self.root_folder = root_folder if root_folder.endswith("/") else root_folder + "/"
        self.auto_cat = True

    @log()
    def edlin(self, script: str, file_name: str) -> list[str]:
        """An improved version of the edlin.

        Args:
            script (str): Edlin commands to run.
            file_name (str): Script creates or edits this file.

        Returns:
            list[str]: The output of the script.

        Examples:
            >>> tool = EdlinTool(".")
            >>> result = tool.edlin("INSERT cat\\nINSERT dog\\nQUIT", "test.md")
            ['cat', 'dog']

            >>> tool = EdlinTool(".")
            >>> result = tool.edlin("1,10 LIST\\nQUIT", "test.md")
            >>> print(result)
            ['cat', 'dog']
        """
        file_name = sanitize_path(file_name)
        # arguments["<file>"],
        # # echo=bool(arguments["--echo"]),
        # halt_on_error=bool(arguments["--halt_on_error"]),
        # macro_file_name=arguments["--macro"],
        # quit_safety=not arguments["--promptless_quit"],
        # # vim_mode=bool(arguments["--vim_mode"]),
        # verbose=bool(arguments["--verbose"]),
        # # blind_mode=bool(arguments["--blind_mode"]),

        #
        # def run(
        #         file_name: Optional[str] = None,
        #         macro_file_name: Optional[str] = None,
        #         echo: bool = False,
        #         halt_on_error: bool = False,
        #         quit_safety: bool = False,
        #         vim_mode: bool = False,
        #         verbose: bool = False,
        #         blind_mode: bool = False,
        # ) -> Dedlin:

        if VERBOSE:
            config = dedlin.configure_logging()
            logging.config.dictConfig(config)
            logger.info("Verbose mode enabled")

        logger.info("Plain mode. UI should be dull.")
        output: list[str] = []

        the_command_generator = StringCommandGenerator(script)

        editor = dedlin.Dedlin(
            inputter=the_command_generator,
            # These should be blank, insert and edit only from the commands.
            insert_document_inputter=None,
            edit_document_inputter=None,
            outputter=lambda text, end=None: output.append(text),
            headless=True,
            untrusted_user=True,
            history=True,
        )

        # No interaction, bot can't recover, answer questions, see realtime trace!
        editor.halt_on_error = True
        editor.quit_safety = False
        editor.echo = False
        # joke!
        editor.vim_mode = False
        # This logging is not for a bot!
        editor.verbose = VERBOSE

        # pylint: disable=broad-except
        try:
            # to broad? Don't register this hook.
            # sys.excepthook = editor.save_on_crash
            editor.entry_point(
                file_name,
            )
            # Bot often forgets to save.
            editor.save_document_safe()
            # must have quit.
        except Exception as the_exception:
            editor.save_on_crash(the_exception, None, None)

            logger.error(traceback.format_exc())
            # output.append(traceback.format_exc())
            editor.save_document_safe()
            raise
        editor.save_document_safe()
        editor.final_report()
        if self.auto_cat:
            feedback = "\n".join(output)
            contents = CatTool(self.root_folder).cat_markdown([file_name])
            return f"Tool feedback: {feedback}\n\nCurrent file contents:\n\n{contents}"
        return output


if __name__ == "__main__":

    def run():
        """Run it"""
        script = """
1 INSERT "Well what of it"
EXIT
"""
        tool = EdlinTool(".")
        result = tool.edlin(script, "test.md")
        print(result)

    run()
