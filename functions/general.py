import logging
from typing import Iterable

import discord

MARKDOWN_CHARS_TO_ESC = {"\\": "\\\\",  # NOTE: this MUST be placed as the first item, or else all subsequent escape \ will be replaced.
                         "*": "\\*", "_": "\\_", "~": "\\~", "`": "\\`", ">": "\\>"
                         }


def get_latency_ms(bot):
    return round(bot.latency * 1000, 1)


def escape_from_md(content):
    if len(content.strip()) == 0:
        # Only whitespace
        return content.strip()
    new_content = content
    for charset in MARKDOWN_CHARS_TO_ESC.items():
        new_content = new_content.replace(*charset)
    logging.info(f"escape_from_md, original={content}, formatted={new_content}")
    return new_content


def dummy_func(*args, **kwargs):
    pass


async def autocomplete_list(ctx: discord.AutocompleteContext, list_of_vals: Iterable):
    return [format for format in list_of_vals if format.startswith(ctx.value.lower())]
