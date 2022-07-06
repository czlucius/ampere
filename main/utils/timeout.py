import signal
from contextlib import contextmanager

import discord

from main.exceptions import TimeoutException
from main.models.safeembed import SafeEmbed


# WARNING: ONLY WORKS ON UNIX SYSTEMS!
@contextmanager
def time_limit(seconds: int, msg="Timed out!"):
    def signal_handler(signum, frame):
        raise TimeoutException(msg)

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


# WARNING: ONLY WORKS ON UNIX SYSTEMS!
# Exits gracefully if time limit exceeds.
@contextmanager
def tle_exit_gracefully(seconds: int, ctx: discord.ApplicationContext, title="Error!", msg="Command timed out.", additional_fields: list = None):
    def signal_handler(signum, frame):
        embed = SafeEmbed(
            title=title,
            description=msg
        )
        if type(additional_fields) == list:
            for field in additional_fields:
                if type(field) == discord.EmbedField:
                    embed.safe_append_field(field, True)
        await ctx.respond()

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
