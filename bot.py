import logging
import os

import discord

from commands.math import Math
from commands.misc import Misc
from commands.dev import Utils

try:
    # Easier to test locally
    with open("token.secret", "r") as envfile:
        TOKEN = envfile.read()
except FileNotFoundError:
    TOKEN = os.getenv("TOKEN")

cogs = [Math, Misc, Utils]
bot = discord.Bot()

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] - [%(levelname)s] - %(message)s')
logging.debug("Start of program")


@bot.event
async def on_ready():
    logging.info(f"{bot.user} has connected to Discord as {bot.user.name}")


for cog in cogs:
    bot.add_cog(cog(bot))
bot.run(TOKEN)
