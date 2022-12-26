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
import io
from contextlib import redirect_stdout

import discord
from aocd import AocdError
from aocd import submit

from components.aoc.parsing import parse_aoc_response
from components.aoc.database import Server
from exceptions import AoCAlreadySolved
from ui.safeembed import SafeEmbed


class AoCModal(discord.ui.Modal):
    def __init__(self, year, day, part, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.year = year
        self.day = day
        self.part = part

        self.add_item(discord.ui.InputText(label="Enter answer here: ", style=discord.InputTextStyle.singleline))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        challenge_identifier = Server.get_challenge_identifier(self.year, self.day, self.part)
        try:
            ans = self.children[0].value

            f = io.StringIO()
            with redirect_stdout(f):
                # Submit answer here...
                submit(ans, part="a" if self.part == 1 else "b", day=self.day, year=self.year, reopen=False)

            response = f.getvalue()
        except AocdError as e:
            response = str(e)
        server = Server.load(interaction.guild_id)
        user_challenges = server.get_challenges(str(interaction.user.id))
        response_code = parse_aoc_response(response)

        if response_code == 1:
            embed = SafeEmbed(title="Answer is correct!", description=f"{interaction.user.mention} got the answer "
                                                                      "correct!")
            # Since this method is idempotent, we can just call it here without an if check.
            try:
                server.add_challenge(str(interaction.user.id), challenge_identifier)
            except AoCAlreadySolved:
                embed.safe_add_field("Note",
                                     f"{interaction.user.mention} has done this challenge before correctly. The score "
                                     "will not be updated.")
        elif response_code == 0:
            embed = SafeEmbed(title="Answer is wrong!", description=f"{interaction.user.mention} got the answer wrong!")
        elif response_code == -1:
            embed = SafeEmbed(title="Indeterminate",
                              description=f"The correctness of the answer that {interaction.user.mention} submitted is "
                                          "indeterminate. Please try again later.")
        elif response_code == -2:
            embed = SafeEmbed(title="Rate limited!",
                              description=f"This question is currently rate limited, please try again later.")

        elif response_code == -3:
            embed = SafeEmbed(title="Input invalid!",
                              description=f"The answer that {interaction.user.mention} submitted "
                                          "is invalid. Please try again.")
        else:
            embed = SafeEmbed(title="Internal server error!", description="An internal server error was encountered "
                                                                          "and your answer is unable to be submitted.")

        print("user challs", user_challenges)

        embed.colour = discord.Colour.yellow()
        embed.safe_add_field("Year", self.year)
        embed.safe_add_field("Day", self.day)
        embed.safe_add_field("Part", self.part)

        await interaction.followup.send(embed=embed)
