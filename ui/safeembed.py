import logging
from typing import Callable

import discord

from exceptions import FieldTooLongError
from functions.general import escape_from_md


def dummy_escape(content):
    return content


class SafeEmbed(discord.Embed):
    def __init__(self,**kwargs):
        if "description" in kwargs:
            if len(kwargs["description"]) > 4096:
                kwargs["description"] = "Field over 4096 characters."

        super().__init__(**kwargs)

    @staticmethod
    def exc_callback():
        raise FieldTooLongError("Field is too long to display in embed.")

    def safe_append_field(self, field: discord.EmbedField, strip_md: bool = False, error: bool = False,
                          exc_callback: Callable = exc_callback):
        processor = escape_from_md if strip_md else dummy_escape

        name = processor(field.name if field.name is not None else "")
        value = processor(field.value if field.value is not None else "")

        logging.info(f"SafeEmbed: value is {value}")

        if len(name) > 1024 or len(value) > 1024:
            # Cannot add this field!
            if error:
                exc_callback()
        else:
            self.add_field(name=name, value=value, inline=field.inline)

    def safe_add_field(self, name: str, value: str, inline: bool = False, strip_md: bool = False, error: bool = False,
                       exc_callback: Callable = exc_callback):

        self.safe_append_field(discord.EmbedField(str(name), str(value), bool(inline)), strip_md=strip_md, error=error,
                               exc_callback=exc_callback)
