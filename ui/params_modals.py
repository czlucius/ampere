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

from models.params_info import ParamsInfo
from ui.safeembed import SafeEmbed


class ParamsModal(discord.ui.Modal):
    def __init__(self, x_class, y_class, embed_callback, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        assert x_class.param_info() is not None or y_class.param_info() is not None
        x_params_info: ParamsInfo = x_class.param_info()
        if x_params_info is not None:
            self.add_item(
                discord.ui.InputText(label=f"Input: {x_params_info.name}", placeholder=x_params_info.placeholder,
                                     min_length=x_params_info.min_length, max_length=x_params_info.max_length,
                                     required=x_params_info.required, style=x_params_info.style)
            )

        y_params_info: ParamsInfo = y_class.param_info()
        if y_params_info is not None:
            self.add_item(
                discord.ui.InputText(label=f"Output: {y_params_info.name}", placeholder=y_params_info.placeholder,
                                     min_length=y_params_info.min_length, max_length=y_params_info.max_length,
                                     required=y_params_info.required, style=y_params_info.style)
            )


        self.x_class = x_class
        self.y_class = y_class
        self.embed_callback = embed_callback


    async def callback(self, interaction: discord.Interaction):
        x_param = y_param = None
        if self.x_class.param_info() is not None and self.y_class.param_info() is not None:
            x_param = self.children[0].value
            y_param = self.children[1].value
        elif self.x_class.param_info() is not None:
            x_param = self.children[0].value
        else:
            y_param = self.children[0].value

        embed: SafeEmbed = self.embed_callback(x_param, y_param)
        if x_param:
            embed.safe_add_field(f"Input parameters ({self.x_class.param_info().name})", x_param, strip_md=True)

        if y_param:
            embed.safe_add_field(f"Output parameters ({self.y_class.param_info().name})", y_param, strip_md=True)

        await interaction.response.send_message(embeds=[embed])

