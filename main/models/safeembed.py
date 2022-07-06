from typing import Callable

import discord

from main.exceptions import InputTooLongException
from main.utils.general import escape_from_md, dummy_func


class SafeEmbed(discord.Embed):
    def safe_append_field(self, field: discord.EmbedField, strip_md: bool = False, error: bool = False,
                          exc_callback: Callable = lambda: InputTooLongException(
                              "Field is too long to display in embed.")):
        processor = escape_from_md if strip_md else dummy_func
        name = processor(field.name)
        value = processor(field.value)

        if len(name) > 1024 or len(value) > 1024:
            # Cannot add this field!
            if error:
                exc_callback
        else:
            self.append_field(field)

    def safe_add_field(self, name: str, value: str, inline: bool = True, strip_md: bool = False, error: bool = False,
                       exc_callback: Callable = lambda: InputTooLongException(
                           "Field is too long to display in embed.")):

        self.safe_append_field(discord.EmbedField(str(name), str(value), bool(inline)), strip_md=strip_md, error=error, exc_callback=exc_callback)
