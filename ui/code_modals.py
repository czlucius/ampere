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

import discord

from models.params_info import ParamsInfo
from ui.safeembed import SafeEmbed


class CodeModal(discord.ui.Modal):
    def __init__(self, embed_callback, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.embed_callback = embed_callback

        self.add_item(discord.ui.InputText(label="Enter program here: ", style=discord.InputTextStyle.multiline))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            code = self.children[0].value
            embed = await self.embed_callback(code)

        except (KeyError, AttributeError) as err:
            # Does not exist, we shall return an error msg.
            embed = SafeEmbed(
                title="Error!",
                description="Input not found.",
                colour=discord.Colour.red()
            )
            logging.error(f"code_modals: error occurred: {err}")

        await interaction.followup.send(embeds=[embed])
