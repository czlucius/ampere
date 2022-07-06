import logging
import os

import discord

from main.commands.math import Math
from main.utils.general import get_latency_ms

TOKEN = os.environ["POETRY_CALCBOT_BOT_TOKEN"]

cogs = [Math]
bot = discord.Bot()


logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] - [%(levelname)s] - %(message)s')
logging.debug("Start of program")


@bot.event
async def on_ready():
    logging.info(f"{bot.user} has connected to Discord as {bot.user.name}")


@bot.slash_command(name="ping", description="Ping the bot")
async def ping(ctx: discord.ApplicationContext):
    latency_ms = get_latency_ms(bot)
    embed = discord.Embed(
        title="Pong!",
        description=f"Latency: {latency_ms} ms"
    )
    logging.info(f"/ping: latency is {latency_ms} ms")

    await ctx.respond(embed=embed)

for cog in cogs:
    bot.add_cog(cog(bot))
bot.run(TOKEN)
