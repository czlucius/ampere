import asyncio

import discord
import sys

from discord.ext import commands
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
from exceptions import InvalidExpressionException, InputInvalidException, FieldTooLongError, EncodeDecodeError
from functions.general import autocomplete_list, wrap_in_codeblocks
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
    "3des-ecb-base64": DESECBToByteArray
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

async def input_format_autocomplete(ctx: discord.AutocompleteContext):
    return await autocomplete_list(ctx, INPUT_FORMATS.keys())

async def output_format_autocomplete(ctx: discord.AutocompleteContext):
    return await autocomplete_list(ctx, OUTPUT_FORMATS.keys())

def produce_cr_autocomplete(langs_available: Set[str]):
    # bflang is not appropriate to be shown in channels, especially where content is not age restricted.
    # Running of bflang is still supported, but the language name would not be shown.
    # Encoded in base64 so that programmers need not see the lang name too.
    langs_available.discard(base64.b64decode("QnJhaW5mdWNr").decode("utf-8"))
    async def cr_autocomplete(ctx: discord.AutocompleteContext):
        return await autocomplete_list(ctx, langs_available)
    return cr_autocomplete

class Utils(BaseCog):
    cr_langs = set()
    def __init__(self, bot):
        self.bot = bot
        self.code_runner = PistonCodeRunner()
        loop = asyncio.get_event_loop()

        self.cr_langs = loop.run_until_complete(self.code_runner.get_lang_names())


    @commands.slash_command(name="x2y", description="Convert from X to Y")
    @discord.option("x", description="Input value")
    @discord.option("x_format", description="Format of input", autocomplete=input_format_autocomplete)
    @discord.option("y_format", description="Format of output", autocomplete=output_format_autocomplete)
    async def x2y(self, ctx: discord.ApplicationContext, x: str, x_format: str, y_format: str):
        logging.info(f"/x2y: x={x}, x_format={x_format}, y_format={y_format}")
        def conversion_present_embed(input_params=None, output_params=None):
            nonlocal x, x_format, y_format
            try:
                if x_format not in INPUT_FORMATS.keys() or y_format not in OUTPUT_FORMATS.keys():
                    # Invalid format. Abort.
                    raise InputInvalidException("Invalid input/output format")
                x = x if x.strip() != "" else "Empty"
                try:
                    intermediate_bytearray_val = INPUT_FORMATS[x_format](x, parameters=input_params).transform()
                    logging.info(f"x2y: intermediate={intermediate_bytearray_val}")
                    y = OUTPUT_FORMATS[y_format](intermediate_bytearray_val, parameters=output_params).transform()
                    logging.info(f"x2y: y= {y}, type={type(y)}")

                except (UnicodeError, UnicodeEncodeError, UnicodeDecodeError):
                    raise EncodeDecodeError("Error in encoding/decoding.")

                y = y if y.strip() != "" else "Empty"
                logging.info(f"/x2y: y = {y} (aft transform), and type={type(y)}")

                embed = SafeEmbed(
                    title="x2y",
                    description=f"Conversion from {x_format} to {y_format}",
                    color=discord.Colour.blue()
                )
                embed.safe_add_field(name="Input", value=x, strip_md=True)
                def output_too_long_err():
                    raise FieldTooLongError(
                        "Output too long. Max 1024 characters.")
                embed.safe_add_field(name="Output", value=y, strip_md=True, error=True, exc_callback=output_too_long_err)

                embed.safe_add_field(name="Input format", value=x_format)
                embed.safe_add_field(name="Output format", value=y_format)

            except (InputInvalidException, InvalidExpressionException, FieldTooLongError, EncodeDecodeError, CipherError) as err:
                errstr = str(err) if str(err).strip() != "" else "An error occurred."
                logging.error(f"/x2y error: {errstr} - {type(err)}")
                embed = SafeEmbed(
                    title="Error!",
                    description=errstr,
                    color=discord.Colour.red()
                )
                embed.safe_add_field(name="Input", value=x, strip_md=True)
                embed.safe_add_field(name="Input format", value=x_format)
                embed.safe_add_field(name="Output format", value=y_format)

            return embed
        x_class = INPUT_FORMATS[x_format]
        y_class = OUTPUT_FORMATS[y_format]
        uses_params = x_class.uses_params() or y_class.uses_params()

        if uses_params:
            modal = ParamsModal(x_class, y_class, conversion_present_embed, title="Parameters")
            await ctx.send_modal(modal)
        else:
            embed = conversion_present_embed()
            await ctx.respond(embed=embed)


    @commands.slash_command(name="run", description="Run code in any language")
    @discord.option("code", description="Contents of program")
    @discord.option("lang", description="Language of program", autocomplete=produce_cr_autocomplete(cr_langs))
    @discord.option("stdin", description="Standard input", required=False)
    @discord.option("args", description="Arguments to supply to program (e.g. in sys.argv)", required=False)
    async def run(self, ctx: discord.ApplicationContext, code, lang, stdin, args):
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

            embed = SafeEmbed(
                title="Program result",
                description=wrap_in_codeblocks(output), # May trigger an error if >1024 chars!
                colour=discord.Colour.teal()
            )
            embed.safe_add_field(
                "Supplied program",
                wrap_in_codeblocks(code)
            )
            embed.safe_add_field(
                "Exit code",
                exit_code
            )
            embed.safe_add_field(
                "Language",
                lang
            )

        else:
            embed = SafeEmbed(
                title="Error!",
                description=error_msg
            )
            logging.error(f"/run: error occurred: {ex_value}")

        await ctx.respond(embed=embed)