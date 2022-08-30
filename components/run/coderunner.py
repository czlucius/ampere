import logging
from typing import Optional

from pyston import PystonClient, File
from pyston.exceptions import InvalidLanguage

from components.run.output import OutputInfo


class PistonCodeRunner:
    ENDPOINT_BASE_URL = "https://emkc.org/api/v2/piston/"  # Can use self-hosted instances in the future.


    def __init__(self):
        self.client = PystonClient(base_url=self.ENDPOINT_BASE_URL)

    async def get_lang_names(self):
        langs = await self.client.languages()
        return langs

    async def run(self, lang: str, contents: str, stdin: Optional[str] = None, args: Optional[str] = None,
                  filename=None):
        """
        Runs code. This function is asynchronous.
        :param str lang: Language of the code (e.g. Python, Kotlin)
        :param str contents: Code to be run.
        :param str stdin: Standard input.
        :param str args: Arguments to the program.
        :param str filename: Optional filename.
        :return: An output object, of class [OutputInfo].
        :raises: InvalidLanguage: Invalid language supplied.
        :raises: TooManyRequests: Code Runner has been rate limited.
        :raises: ExecutionError: An error has occurred in the execution of the program.
        :raises: InternalServerError: Internal server error occurred.
        :raises: UnexpectedError: An unexpected error occurred.
        """


        # We allow codeblocks in the code field, as it has syntax highlighting when inputting the code.
        # However, codeblocks are explicitly removed.
        langs = await self.get_lang_names()
        if lang not in langs:
            raise InvalidLanguage(f"No such language: {lang}") # We shall use Pyston's exceptions; there is no need to create our own.

        if contents.startswith("```") and contents.endswith("```"):
            new_contents = contents.strip("```")
            new_contents = "\n".join(new_contents.splitlines()[1:]) # The 1st line will still have some language e.g. ```(py) even as the ``` is removed.
            contents = new_contents

        code = [File(contents, filename)]
        output_obj = await self.client.execute(lang, code, stdin=stdin, args=args, compile_timeout=15_000,
                                               run_timeout=60_000)

        detected_lang = output_obj.langauge
        run_stage = output_obj.run_stage

        output = run_stage.output
        exit_code = run_stage.code
        signal = run_stage.signal

        logging.info(f"PistonCodeRunner - {output_obj} - success={output_obj.success}")
        logging.info(f"PistonCodeRunner - {output} - dl={detected_lang} ")

        out_formatted = OutputInfo(
            output, exit_code, signal, detected_lang, run_stage, output_obj.compile_stage
        )

        return out_formatted
