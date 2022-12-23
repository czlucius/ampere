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

import discord

from ui.aoc_modals import AoCModal


class AoCSubmitButton(discord.ui.View):

    def __init__(self, year, day, part, *items):
        super().__init__(*items)
        self.year = year
        self.day = day
        self.part = part

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.primary, emoji="📤")
    async def button_callback(self, button, interaction):
        # Send a message when the button is clicked
        await interaction.response.send_modal(AoCModal(self.year, self.day, self.part, title="Answer"))
