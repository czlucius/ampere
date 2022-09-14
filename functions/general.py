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
from typing import Iterable

import discord

MARKDOWN_CHARS_TO_ESC = {"\\": "\\\\",  # NOTE: this MUST be placed as the first item, or else all subsequent escape \ will be replaced.
                         "*": "\\*", "_": "\\_", "~": "\\~", "`": "\\`", ">": "\\>"
                         }

LANGS_REPLACEMENTS = {"python2": "py"}
def get_latency_ms(bot):
    return round(bot.latency * 1000, 1)


def escape_from_md(content: str):
    if len(content.strip()) == 0:
        # Only whitespace
        return content.strip()
    new_content = content
    for charset in MARKDOWN_CHARS_TO_ESC.items():
        new_content = new_content.replace(*charset)
    logging.info(f"escape_from_md, original={content}, formatted={new_content}")
    return new_content

def wrap_in_codeblocks(content: str, lang: str = ""):
    if len(content) == 0:
        return content # We cannot have empty content in a codeblock, it will just show ``````
    content = content.replace("```", "`\u200d`\u200d`") # We replace with ZWJ between so the codeblock will not escape even if there is ```.
    content = f"```{lang}\n" + content + "\n```" # Wrap content in codeblocks.
    return content


def lang_for_syntax_highlighting(lang: str):
    for original, new in LANGS_REPLACEMENTS.items():
        if lang == original:
            lang = new
    return lang

def dummy_func(*args, **kwargs):
    pass


async def autocomplete_list(ctx: discord.AutocompleteContext, list_of_vals: Iterable[str]):
    return [format for format in list_of_vals if format.lower().startswith(ctx.value.lower())]
