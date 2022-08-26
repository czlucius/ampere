import random

import discord
from discord.ext import commands

from commands.basecog import BaseCog
from conversions.decode.BinaryToByteArray import BinaryToByteArray
from conversions.decode.HexToByteArray import HexToByteArray
from conversions.decode.TextToByteArray import TextToByteArray
from conversions.decode.baseencoded import *
from conversions.decode.caesar import CaesarCipherToByteArray
from conversions.encode.ByteArrayToBinary import ByteArrayToBinary
from conversions.encode.ByteArrayToHex import ByteArrayToHex
from conversions.encode.ByteArrayToText import ByteArrayToText
from conversions.encode.baseencoded import *
from conversions.encode.caesar import ByteArrayToCaesarCipher
from conversions.encode.cipher import *
from conversions.encode.hashing import *
from conversions.decode.cipher import *
from exceptions import InvalidExpressionException, InputInvalidException, FieldTooLongError, EncodeDecodeError
from functions.general import autocomplete_list
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

class Utils(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        # Initialise the docker container for translation.

    @commands.slash_command(name="rng", description="Generate random numbers")
    @discord.option("lower_bound", description="Lower bound of range of random numbers",
                    type=discord.SlashCommandOptionType.integer)
    @discord.option("upper_bound", description="Upper bound of range of random numbers",
                    type=discord.SlashCommandOptionType.integer)
    @discord.option("step",
                    description="Interval in sequence of numbers for generator to choose from. Positive integers only.",
                    type=discord.SlashCommandOptionType.integer, required=False)
    async def rng(self, ctx: discord.ApplicationContext, lower_bound: int, upper_bound: int, step: int):
        logging.info(f"/rng: lower_bound={lower_bound}, upper_bound={upper_bound}, step={step}")
        try:
            if upper_bound <= lower_bound:
                raise InvalidExpressionException("Upper bound must be greater than lower bound!")
            elif step and step < 0:
                raise InvalidExpressionException("Step must be postive.")
            random_no = random.randrange(lower_bound, upper_bound, step if step else 1)

            embed = discord.Embed(
                title="Random Number Generator",
                description=f"Number generated: {random_no}",
                color=discord.Colour.green()
            )

            embed.add_field(
                name="Lower bound",
                value=str(lower_bound)
            )

            embed.add_field(
                name="Upper bound",
                value=str(upper_bound)
            )
            if step:
                embed.add_field(
                    name="Step",
                    value=str(step)
                )
        except InvalidExpressionException as err:
            embed = discord.Embed(
                title="Error!",
                description=str(err)
            )

        await ctx.respond(embed=embed)

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
