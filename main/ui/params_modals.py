import discord

from main.ui.params_info import ParamsInfo
from main.models.safeembed import SafeEmbed


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

