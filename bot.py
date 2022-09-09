import logging
import os

import discord

from commands.math import Math
from commands.misc import Misc
from commands.dev import Dev
from commands.rand import Rand

from dotenv import load_dotenv

load_dotenv("secret.env")
TOKEN = os.getenv("TOKEN")

cogs = [Math, Misc, Dev, Rand]
bot = discord.Bot()

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] - [%(levelname)s] - %(message)s')
logging.debug("Start of program")


@bot.event
async def on_ready():
    logging.info(f"{bot.user} has connected to Discord as {bot.user.name}")


for cog in cogs:
    bot.add_cog(cog(bot))
bot.run(TOKEN)
