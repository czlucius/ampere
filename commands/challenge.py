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
import datetime

import discord
from aocd.models import Puzzle
from discord import commands
from markdownify import markdownify as md

from commands.basecog import BaseCog
from components.aoc.database import Server
from components.aoc.scraping import scrape_challenge
from exceptions import ChallengeUnavailableException
from ui.aoc_btn import AoCSubmitButton
from ui.safeembed import SafeEmbed

this_year = datetime.date.today().year
# As per Wikipedia, AoC started on 2015.
# https://en.wikipedia.org/wiki/Advent_of_Code
aoc_years = list([str(x) for x in range(this_year, 2014, -1)])
aoc_days = list([str(x) for x in range(1, 26)])


class Challenge(BaseCog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="aoc", description="Get challenges from Advent of Code. Do not spam.")
    @discord.option("year", description="Year of challenge", choices=aoc_years)
    @discord.option("day", description="Day of challenge", choices=aoc_days)
    @discord.option("part", description="Part 1 or 2", choices=["1", "2"], default="1")
    async def aoc(self, ctx: discord.ApplicationContext, year: str, day: str, part: str):
        await ctx.defer()
        year = int(year)
        day = int(day)
        part = int(part)
        puzzle = Puzzle(year=year, day=day)
        data_file = None

        try:
            contents = await scrape_challenge(year, day, part)

            challenge = md(contents)
            input_data = puzzle.input_data  # Input data will be cached by AoCD

            path = f"/tmp/aoc{year}{day}{part}"
            with open(path, "w") as f:
                f.write(input_data)

            data_file = discord.File(path)

            main_desc = f"**Challenge text**\n{challenge}\n" \
                        "**Input data**\nInput data is attached as a file."

            embed = SafeEmbed(
                title="Advent of Code Challenge",
                description=main_desc,
                color=discord.Colour.yellow()
            )
            embed.safe_add_field(name="Day", value=str(day), strip_md=True)
            embed.safe_add_field(name="Year", value=str(year), strip_md=True)
            embed.safe_add_field(name="Part", value=str(part), strip_md=True)
        except ChallengeUnavailableException as e:
            embed = SafeEmbed(
                title="Error",
                description=str(e),
                color=discord.Colour.red()
            )

        await ctx.respond(
            embed=embed,
            files=[data_file] if data_file else [],
            view=AoCSubmitButton(year, day, part) if data_file else None
        )

    @commands.slash_command(name="aoc_leaderboard", description="Get leaderboard for Advent of Code submissions "
                                                                "through Ampere.")
    @discord.option("user", description="Check score of specific user. Mention a specific user.",
                    input_type=discord.SlashCommandOptionType.user, required=False)
    async def aoc_leaderboard(self, ctx: discord.ApplicationContext, user: str):
        await ctx.defer()
        print(ctx.guild_id)
        server = Server.load(ctx.guild_id)
        if not user:
            desc = "Leaderboard for AoC submissions through Ampere\n\n"

            print(server.leaderboard)
            if len(server.leaderboard.keys()) == 0:
                # No users
                desc += "No users found.\n"
            else:
                for index, user_id in enumerate(server.get_top_10()):
                    member_obj = ctx.guild.get_member(int(user_id))
                    member_points = server.get_user_score(user_id)
                    desc += f"{index + 1}. {member_obj.name}({member_obj.mention}) - {member_points} point(s)"
            embed = SafeEmbed(
                title="Advent of Code Leaderboard",
                description=desc,
                color=discord.Colour.yellow()
            )
        else:
            user_id = user.strip("<@").strip(">")
            isnum = True
            try:
                int(user_id)
            except ValueError:
                isnum = False

            if not isnum:
                # user does not exist
                embed = SafeEmbed(
                    title="User does not exist",
                    description=f"{user} does not exist.",
                    color=discord.Colour.red()
                )
            elif ctx.guild.get_member(int(user_id)) is None:
                embed = SafeEmbed(
                    title="User does not exist",
                    description=f"{user} does not exist.",
                    color=discord.Colour.red()
                )
            else:
                member = ctx.guild.get_member(int(user_id))
                score = server.get_user_score(user_id)
                embed = SafeEmbed(
                    title=f"Score for {member.name}",
                    description=f"{user}'s score is {score}"
                )

        await ctx.respond(
            embed=embed
        )
