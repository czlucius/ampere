import logging, os
import discord

from py_expression_eval import Parser

from exceptions import InvalidExpressionException, TimeoutException
from utils.general import get_latency_ms, escape_from_md
from utils.timeout import time_limit

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] - [%(levelname)s] - %(message)s')
logging.debug('Start of program')

TOKEN = os.environ["POETRY_CALCBOT_BOT_TOKEN"]
bot = discord.Bot()

parser = Parser()


@bot.event
async def on_ready():
    logging.info(f"{bot.user} has connected to Discord as {bot.user.name}")


@bot.slash_command(name="ping", description="Ping the bot")
async def ping(ctx):
    latency_ms = get_latency_ms(bot)
    embed = discord.Embed(
        title="Pong!",
        description=f"Latency: {latency_ms} ms"
    )
    logging.info(f"/ping: latency is {latency_ms} ms")

    await ctx.respond(embed=embed)


@bot.slash_command(name="hello", description="Says hello")
async def hello(ctx):
    logging.info("/hello: Hello!")

    await ctx.respond("Hello!")


@bot.slash_command(name="calculate", description="Calculate expression")
@discord.option("expression", description="Enter a mathematical expression to be evaluated")
@discord.option("precision", discord.SlashCommandOptionType.integer,
                description="Specify the precision in decimal points. (e.g. 3)", required=False)
async def calculate(ctx, expression, precision):
    logging.info(f"/calculate: expression={expression}, precision={precision}")

    try:
        expr_length = len(escape_from_md(expression))
        expression_too_long = expr_length > 1024

        with time_limit(2, "Command timed out."):

            try:
                parsed = parser.parse(expression)
            except TimeoutException:
                raise
            except Exception:
                raise InvalidExpressionException("Parsing error.")

            try:
                # NOTE: this may introduce a DDoS vulnerability as people may try to calculate a very large and expensive expression which will freeze the machine.
                result = parsed.evaluate({})
                logging.info(f"/calculate: result={result}")
            except TimeoutException:
                raise
            except Exception:
                raise InvalidExpressionException("Invalid expression.")

            # Round to set precision.
            if precision:

                try:
                    precision_int = int(precision)
                    result = format(result, f".{precision_int}f")
                except ValueError:
                    raise InvalidExpressionException("Invalid precision.")

            result_length = len(str(result))
            if result_length > 1024:
                raise InvalidExpressionException("Result too long. Max 1024 characters.")

            else:
                embed = discord.Embed(
                    title="Expression result",
                    color=discord.Colour.blue()
                )
                if not expression_too_long:
                    embed.add_field(name="Original expression", value=escape_from_md(expression))
                if precision:
                    embed.add_field(name="Precision", value=precision)
                embed.add_field(name="Result", value=result)

    except (InvalidExpressionException, TimeoutException) as err:

        logging.error(f"/calculate error in parsing: {err} - {type(err)}")
        embed = discord.Embed(
            title="Error!",
            description=str(err),
            color=discord.Colour.red()
        )
        if not expression_too_long:
            embed.add_field(name="Expression", value=escape_from_md(expression))
        if precision:
            embed.add_field(name="Precision", value=precision)

    await ctx.respond(embed=embed)


bot.run(TOKEN)
