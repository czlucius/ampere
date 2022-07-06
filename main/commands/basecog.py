import logging

from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self):
        # Log startup:
        logging.info("%s has started up" % type(self).__name__)
