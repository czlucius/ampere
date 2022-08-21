from discord.ext import commands
from py_expression_eval import Parser

from commands.basecog import BaseCog
from exceptions import InvalidExpressionException, InputTooLongException
from ui.safeembed import SafeEmbed

from functions.general import *
from functions.timeout import tle_exit_gracefully

CONSTANTS_VALS = {"π": 3.14159265358979323846264338327950288, "e": 2.71828182845904523536028747135266249,
                  "ϕ": 1.61803398874989484820458683436563811, "Ω": 0.56714329040978387299996866221035554}


async def get_constants_keys(ctx: discord.AutocompleteContext):
    return await autocomplete_list(ctx, CONSTANTS_VALS)


class Math(BaseCog):

    def __init__(self, bot):
        self.bot = bot
        self.parser = Parser()

    @commands.slash_command(name="calculate", description="Calculate expression")
    @discord.option("expression", description="Enter a mathematical expression to be evaluated")
    @discord.option("precision", discord.SlashCommandOptionType.integer,
                    description="Specify the precision in decimal points. (e.g. 3)", required=False)
    async def calculate(self, ctx: discord.ApplicationContext, expression: str, precision: int):
        logging.info(f"/calculate: expression={expression}, precision={precision}")

        try:

            with tle_exit_gracefully(2, ctx):

                try:
                    parsed = self.parser.parse(expression)
                except Exception:
                    raise InvalidExpressionException("Parsing error.")

                try:
                    result = parsed.evaluate({})
                    logging.info(f"/calculate: result={result}")
                except Exception:
                    raise InvalidExpressionException("Invalid expression.")

                if precision:
                    try:
                        precision_int = int(precision)
                        result = format(result, f".{precision_int}f")
                    except ValueError:
                        raise InvalidExpressionException("Invalid precision.")

                embed = SafeEmbed(
                    title="Expression result",
                    color=discord.Colour.blue()
                )
                embed.safe_add_field(name="Original expression", value=expression, strip_md=True)
                if precision:
                    embed.safe_add_field(name="Precision", value=str(precision))

                def if_err():
                    raise InputTooLongException(
                                         "Result too long. Max 1024 characters.")

                embed.safe_add_field(name="Result", value=result, error=True, strip_md=True,
                                     exc_callback=if_err)

        except (InvalidExpressionException, InputTooLongException) as err:

            logging.error(f"/calculate error in parsing: {err} - {type(err)}")
            embed = SafeEmbed(
                title="Error!",
                description=str(err),
                color=discord.Colour.red()
            )
            embed.safe_add_field(name="Expression", value=expression, strip_md=True)
            if precision:
                embed.safe_add_field(name="Precision", value=str(precision), strip_md=True)

        await ctx.respond(embed=embed)

    @commands.slash_command(name="constants", description="Get values of constants")
    @discord.option("name", autocomplete=get_constants_keys, description="Name of constant")
    async def constants(self, ctx: discord.ApplicationContext, name: str):

        if name in CONSTANTS_VALS.keys():
            value = CONSTANTS_VALS[name]
            embed = SafeEmbed(
                title=name,
                description=value
            )
        else:
            embed = SafeEmbed(
                title="Error!",
                description="Constant not found."
            )

        logging.info(f"/constants: name={name} embed_desc={embed.description}")

        await ctx.respond(embed=embed)
