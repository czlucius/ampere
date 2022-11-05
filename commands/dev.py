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

import asyncio
import logging

import discord
import sys

from aiohttp import ContentTypeError
from discord.ext import commands
from pyston import File
from pyston.exceptions import *
from typing import Set

from commands.basecog import BaseCog
from components.conversions.decode.BinaryToByteArray import BinaryToByteArray
from components.conversions.decode.HexToByteArray import HexToByteArray
from components.conversions.decode.TextToByteArray import TextToByteArray
from components.conversions.decode.baseencoded import *
from components.conversions.decode.caesar import CaesarCipherToByteArray
from components.conversions.encode.ByteArrayToBinary import ByteArrayToBinary
from components.conversions.encode.ByteArrayToHex import ByteArrayToHex
from components.conversions.encode.ByteArrayToText import ByteArrayToText
from components.conversions.encode.baseencoded import *
from components.conversions.encode.caesar import ByteArrayToCaesarCipher
from components.conversions.encode.cipher import *
from components.conversions.encode.hashing import *
from components.conversions.decode.cipher import *
from components.run.coderunner import PistonCodeRunner
from components.run.libdl import download_py_whl, NoSuitablePackageException
from exceptions import InvalidExpressionException, InputInvalidException, FieldTooLongError, EncodeDecodeError
from functions.general import autocomplete_list, wrap_in_codeblocks, lang_for_syntax_highlighting
from ui.code_modals import CodeModal
from ui.params_modals import ParamsModal
from ui.safeembed import SafeEmbed

INPUT_FORMATS = {
    "binary": BinaryToByteArray,
    "hex": HexToByteArray,
    "text": TextToByteArray,
    "base32": Base32ToByteArray,
    "base45": Base45ToByteArray,
    "base58": Base58ToByteArray,
    "base62": Base62ToByteArray,
    "base64": Base64ToByteArray,
    "ascii85": Ascii85ToByteArray,
    "caesar-cipher": CaesarCipherToByteArray,
    "aes-ecb-base64": AESECBToByteArray,
    "des-ecb-base64": DESECBToByteArray,
    "3des-ecb-base64": DES3ECBToByteArray
}


OUTPUT_FORMATS = {
    "binary": ByteArrayToBinary,
    "hex": ByteArrayToHex,
    "text": ByteArrayToText,
    "base32": ByteArrayToBase32,
    "base45": ByteArrayToBase45,
    "base58": ByteArrayToBase58,
    "base62": ByteArrayToBase62,
    "base64": ByteArrayToBase64,
    "ascii85": ByteArrayToAscii85,
    "caesar-cipher": ByteArrayToCaesarCipher,
    "sha256": ByteArrayToSHA256,
    "md5": ByteArrayToMD5,
    "sha1": ByteArrayToSHA1,
    "sha512": ByteArrayToSHA512,
    "aes-ecb-base64": ByteArrayToAESECB,
    "des-ecb-base64": ByteArrayToDESECB,
    "3des-ecb-base64": ByteArrayToDES3ECB
}

loop = asyncio.get_event_loop()

cr_langs = loop.run_until_complete(PistonCodeRunner().get_lang_names()) # Just create a dummy code runner object to get langs
# logging.info(f"Dev - langs are {cr_langs}")

async def input_format_autocomplete(ctx: discord.AutocompleteContext):
    return await autocomplete_list(ctx, INPUT_FORMATS.keys())

async def output_format_autocomplete(ctx: discord.AutocompleteContext):
    return await autocomplete_list(ctx, OUTPUT_FORMATS.keys())

def produce_cr_autocomplete(langs_available: Set[str]):

    # bflang is not appropriate to be shown in channels, especially where content is not age restricted.
    # Running of bflang is still supported, but the language name would not be shown.
    # Encoded in base64 so that programmers need not see the lang name too.
    langs_available.discard(base64.b64decode("YnJhaW5mdWNr").decode("utf-8"))

    print(f"produce_cr_autocomplete - langs are {langs_available}")
    async def cr_autocomplete(ctx: discord.AutocompleteContext):
        return await autocomplete_list(ctx, list(langs_available))
    return cr_autocomplete


class Dev(BaseCog):

    def __init__(self, bot):
        self.bot = bot
        self.code_runner = PistonCodeRunner()




    @commands.slash_command(name="conv", description="Convert from one format to another")
    @discord.option("i", description="Input value")
    @discord.option("i_format", description="Format of input", autocomplete=input_format_autocomplete)
    @discord.option("o_format", description="Format of output", autocomplete=output_format_autocomplete)
    async def conv(self, ctx: discord.ApplicationContext, i: str, i_format: str, o_format: str):
        logging.info(f"/conv: x={i}, x_format={i_format}, y_format={o_format}")
        def conversion_present_embed(input_params=None, output_params=None):
            nonlocal i, i_format, o_format
            try:
                if i_format not in INPUT_FORMATS.keys() or o_format not in OUTPUT_FORMATS.keys():
                    # Invalid format. Abort.
                    raise InputInvalidException("Invalid input/output format")
                i = i if i.strip() != "" else "Empty"
                try:
                    intermediate_bytearray_val = INPUT_FORMATS[i_format](i, parameters=input_params).transform()
                    logging.info(f"conv: intermediate={intermediate_bytearray_val}")
                    o = OUTPUT_FORMATS[o_format](intermediate_bytearray_val, parameters=output_params).transform()
                    logging.info(f"conv: o= {o}, type={type(o)}")

                except (UnicodeError, UnicodeEncodeError, UnicodeDecodeError):
                    raise EncodeDecodeError("Error in encoding/decoding.")

                o = o if o.strip() != "" else "Empty"
                logging.info(f"/conv: o = {o} (aft transform), and type={type(o)}")

                embed = SafeEmbed(
                    title="conv",
                    description=f"Conversion from {i_format} to {o_format}",
                    color=discord.Colour.blue()
                )
                embed.safe_add_field(name="Input", value=i, strip_md=True)
                def output_too_long_err():
                    raise FieldTooLongError(
                        "Output too long. Max 1024 characters.")
                embed.safe_add_field(name="Output", value=o, strip_md=True, error=True, exc_callback=output_too_long_err)

                embed.safe_add_field(name="Input format", value=i_format)
                embed.safe_add_field(name="Output format", value=o_format)

            except (InputInvalidException, InvalidExpressionException, FieldTooLongError, EncodeDecodeError, CipherError) as err:
                errstr = str(err) if str(err).strip() != "" else "An error occurred."
                logging.error(f"/conv error: {errstr} - {type(err)}")
                embed = SafeEmbed(
                    title="Error!",
                    description=errstr,
                    color=discord.Colour.red()
                )
                embed.safe_add_field(name="Input", value=i, strip_md=True)
                embed.safe_add_field(name="Input format", value=i_format)
                embed.safe_add_field(name="Output format", value=o_format)

            return embed
        x_class = INPUT_FORMATS[i_format]
        y_class = OUTPUT_FORMATS[o_format]
        uses_params = x_class.uses_params() or y_class.uses_params()

        if uses_params:
            modal = ParamsModal(x_class, y_class, conversion_present_embed, title="Parameters")
            await ctx.send_modal(modal)
        else:
            embed = conversion_present_embed()
            await ctx.respond(embed=embed)


    @commands.slash_command(name="run", description="Run code in any language")
    @discord.option("lang", description="Language of program", autocomplete=produce_cr_autocomplete(cr_langs))
    @discord.option("code", description="Contents of program, omit for multiline dialog", required=False)
    @discord.option("stdin", description="Standard input", required=False)
    @discord.option("args", description="Arguments to supply to program (e.g. in sys.argv)", required=False)
    async def run(self, ctx: discord.ApplicationContext, lang, code, stdin, args):
        async def run_present_embed(code=code):
            nonlocal lang, stdin, args
            runner = self.code_runner
            error_msg = None
            out = None


            try:
                out = await runner.run(lang, code, stdin, args)
            except TooManyRequests:
                error_msg = "Bot has exceeded its rate limit. Please try again shortly."
            except InvalidLanguage:
                error_msg = f"No such language: {lang}"
            except InternalServerError:
                error_msg = "Internal server error occurred."
            except ExecutionError as err:
                error_msg = f"Execution error: {err}"
            except UnexpectedError as err:
                error_msg = f"An unexpected error has occurred: {err}"
            ex_type, ex_value, traceback = sys.exc_info()
            if not error_msg:
                output = out.output
                exit_code = out.exit_code
                # original code, exit status, lang

                output_wrapped = wrap_in_codeblocks(output) if output else "No output detected"
                if len(output_wrapped) > 4096:
                    output_wrapped = output_wrapped[:4062] + "... truncated at 4096 chars ..." + "```"

                embed = SafeEmbed(
                    title="Program result",
                    description=output_wrapped,
                    colour=discord.Colour.teal()
                )

                embed.safe_add_field(
                    "Supplied program",
                    wrap_in_codeblocks(code, lang_for_syntax_highlighting(lang))
                )
                embed.safe_add_field(
                    "Exit code",
                    exit_code
                )

                if stdin:
                    embed.safe_add_field("Input (stdin)", stdin)
                if args:
                    embed.safe_add_field("Arguments", args)
                if lang == base64.b64decode("YnJhaW5mdWNr").decode("utf-8"):
                    # bflang
                    lang = "bflang"
                embed.safe_add_field(
                    "Language",
                    lang
                )

            else:
                embed = SafeEmbed(
                    title="Error!",
                    description=error_msg,
                    colour=discord.Colour.red()
                )
                logging.error(f"/run: error occurred: {ex_value}")
            return embed

        if code:
            await ctx.defer()
            await ctx.respond(embed=await run_present_embed(code))
        else:
            modal = CodeModal(run_present_embed, title="Code")
            await ctx.send_modal(modal)


    @commands.slash_command(name="py_with_external_libs", description="Run Python3 code with libraries from PyPI")
    @discord.option("lib", description="Library to include")
    @discord.option("code", description="Contents of program, omit for multiline dialog", required=False)
    @discord.option("stdin", description="Standard input", required=False)
    @discord.option("args", description="Arguments to supply to program (e.g. in sys.argv)", required=False)
    async def py_with_external_libs(self, ctx: discord.ApplicationContext, lib, code, stdin, args):
        async def pyrun_present_embed(code=code):
            runner = self.code_runner
            error_msg = None
            out = None

            try:
                whl = await download_py_whl(lib)
                filename = whl[0]
                lib_whl_contents = whl[1]
                lib_whl_contents_b64 = base64.a85encode(lib_whl_contents).decode("utf-8")
                files_extra = [File(lib_whl_contents_b64, "package.whl.a85")]

                patched_code = f"""import base64, os, sys, subprocess
with open("package.whl.a85", "rb") as file:
    decoded_file = base64.a85decode(file.read())
with open("{filename}", "wb") as file: 
    file.write(decoded_file)
os.mkdir("pkg-dir")
cwd = os.getcwd()
pkg_dir = os.path.join(cwd, "pkg-dir")
subprocess.run(["python3", "-m", "pip", "install", "--target=" + pkg_dir,  "{filename}"])
sys.path.append(pkg_dir)
print()
print("--- Execution ---")
"""
                patched_code += code
                out = await runner.run("python", patched_code, stdin, args, other_files=files_extra, run_timeout=360_000) # Run for 6 min to allow package to download
            except TooManyRequests:
                error_msg = "Bot has exceeded its rate limit. Please try again shortly."
            except InternalServerError:
                error_msg = "Internal server error occurred."
            except ExecutionError as err:
                error_msg = f"Execution error: {err}"
            except UnexpectedError as err:
                error_msg = f"An unexpected error has occurred: {err}"
            except NoSuitablePackageException as err:
                error_msg = str(err) # We already made sure error msgs are presentable in libdl.py.
            except ContentTypeError: # It'll return a HTML 404 page if file is too large, and this error will be thrown
                error_msg = "Library is too large"

            ex_type, ex_value, traceback = sys.exc_info()
            if not error_msg:
                output = out.output
                exit_code = out.exit_code
                # original code, exit status, lang
                output_wrapped = wrap_in_codeblocks(output)
                if len(output_wrapped) > 4096:
                    output_wrapped = output_wrapped[:4062] + "... truncated at 4096 chars ..." + "```"


                embed = SafeEmbed(
                    title="Program result",
                    description=output_wrapped,
                    colour=discord.Colour.dark_blue()
                )
                embed.safe_add_field(
                    "Supplied program",
                    wrap_in_codeblocks(code, "python")
                )
                embed.safe_add_field(
                    "Exit code",
                    exit_code
                )
                embed.safe_add_field(
                    "Language",
                    "py-with-external-libs"
                )
                embed.safe_add_field(
                    "Library included",
                    lib
                )

            else:
                embed = SafeEmbed(
                    title="Error!",
                    description=error_msg
                )
                logging.error(f"/py_with_libs: error occurred: {ex_value}")
            return embed
        if code:
            await ctx.defer()
            await ctx.respond(embed=await pyrun_present_embed(code))
        else:
            modal = CodeModal(pyrun_present_embed, title="Code")
            await ctx.send_modal(modal)

