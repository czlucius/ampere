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

import signal
from contextlib import contextmanager

import discord

from exceptions import TimeoutException
from ui.safeembed import SafeEmbed


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
        ctx.respond(embed=embed)

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
