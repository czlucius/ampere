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
import random
import discord
from discord import commands

from commands.basecog import BaseCog
from exceptions import InvalidExpressionException


class Rand(BaseCog):
    def __init__(self, bot):
        self.bot = bot



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