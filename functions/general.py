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

LANGS_REPLACEMENTS = {"python2": "py", "sqlite3": "sql"}
def get_latency_ms(bot):
    return round(bot.latency * 1000, 1)


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

def filter_codeblocks(content: str):
    if code.startswith("```") and code.endswith("```"):
        new_contents = contents.strip("```").splitlines()
        if len(new_contents) > 1:
            # If there is more than one line, then a language is specified
            return "\n".join(new_contents[1:])
        elif len(new_contents) == 1:
            # If it is only one line, then a language is not specified
            return new_contents[0]
        else:
            return ""
        
def truncate(content: str):
    # To prevent spam
    if len(content) > 4096:
        content = content[:4062] + "... truncated at 4096 chars ..." + "```"
    split = content.splitlines()
    if len(split) > 50:
        content = "\n".join(split[:50])
        if len(content) > 4063:
            content = content[:4063] + "\n... truncated at 50 lines ..."
        else:
            content = content + "\n... truncated at 50 lines ..."
    return content
def dummy_func(*args, **kwargs):
    pass


async def autocomplete_list(ctx: discord.AutocompleteContext, list_of_vals: Iterable[str]):
    return [format for format in list_of_vals if format.lower().startswith(ctx.value.lower())]
