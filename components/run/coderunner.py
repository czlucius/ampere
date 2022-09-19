
#   A multi-purpose Discord Bot written with Python and pycord.
#   Copyright (C) 2022 czlucius (lcz5#3392)
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from typing import Optional, List

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
                  filename=None, other_files: List[File] = None, compile_timeout=60_000, run_timeout = 60_000):
        """
        Runs code. This function is asynchronous.
        :param str lang: Language of the code (e.g. Python, Kotlin)
        :param str contents: Code to be run.
        :param str stdin: Standard input.
        :param str args: Arguments to the program.
        :param str filename: Optional filename.
        :param str other_files: Other files to include.
        :param run_timeout: Run timeout
        :param compile_timeout: Compule timeout.
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
            new_contents = contents.strip("```").splitlines()
            if len(new_contents) > 1:
                # If there is more than one line, then a language is specifies
                contents = "\n".join(new_contents[1:])
            else:
                # If it is only one line, then a language is not specified
                contents = new_contents[0]

        code = [File(contents, filename)]
        if other_files:
            code.extend(other_files)

        output_obj = await self.client.execute(lang, code, stdin=stdin, args=args, compile_timeout=compile_timeout,
                                               run_timeout=run_timeout)

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
