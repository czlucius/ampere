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
