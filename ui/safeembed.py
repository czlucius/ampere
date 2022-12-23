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
from typing import Callable

import discord
from discord.utils import escape_markdown

from exceptions import FieldTooLongError


def dummy_escape(content: str) -> str:
    return content


class SafeEmbed(discord.Embed):
    def __init__(self, **kwargs):
        if "description" in kwargs:
            if len(kwargs["description"]) > 4096:
                kwargs["description"] = "Field over 4096 characters."

        super().__init__(**kwargs)

    @staticmethod
    def exc_callback():
        raise FieldTooLongError("Field is too long to display in embed.")

    def safe_append_field(self, field: discord.EmbedField, strip_md: bool = False, error: bool = False,
                          exc_callback: Callable = exc_callback):
        processor = escape_markdown if strip_md else dummy_escape

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
