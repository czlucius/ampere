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

from urllib.error import HTTPError
from libretranslatepy import LibreTranslateAPI
from commands.basecog import BaseCog
from discord.ext import commands

from exceptions import InvalidOptionException
from functions.io import json_open
from ui.safeembed import SafeEmbed
from functions.general import get_latency_ms, autocomplete_list


class Misc(BaseCog):

    def __init__(self, bot):
        self.bot = bot
    # @commands.slash_command(name="translate", description="Translate between languages")
    # @discord.option("text", description="Text to translate")
    # @discord.option("source", description="Language you're translating from", autocomplete=autocomplete_source_lang)
    # @discord.option("dest", description="Language you're translating to", autocomplete=autocomplete_dest_lang)
    # async def translate(self, ctx: discord.ApplicationContext, text: str, source: str, dest: str):
    #     await ctx.defer() # May take > 3 seconds
    #     try:
    #         if source not in lt_source_langs:
    #             raise InvalidOptionException("Invalid source language!")
    #         if dest not in lt_langs:
    #             raise InvalidOptionException("Invalid target language!")
    #         logging.info(f"/translate - from{lt_source_langs[source]} - to{lt_source_langs[dest]}")
    #
    #         translated = lt_client.translate(text,  lt_source_langs[source], lt_source_langs[dest])
    #         embed = SafeEmbed(
    #             title="Translated text",
    #             description=translated
    #         )
    #         embed.safe_add_field("Original text", text)
    #         embed.safe_add_field("From", source)
    #         embed.safe_add_field("To", dest)
    #         embed.set_footer(text="Powered by LibreTranslate")
    #     except InvalidOptionException as err:
    #         embed = SafeEmbed(
    #             title="Error!",
    #             description=str(err),
    #             colour=discord.Colour.red()
    #         )
    #         logging.error(f"/translate: error occurred - {err} - {type(err)}")
    #     except HTTPError as err:
    #         embed = SafeEmbed(
    #             title="Error!",
    #             description="API endpoint error",
    #             colour=discord.Colour.red()
    #         )
    #         logging.error(f"/translate: error occurred - {err} - {type(err)}")
    #
    #
    #     await ctx.respond(embed=embed)
    #


    @commands.slash_command(name="ping", description="Ping the bot")
    async def ping(self, ctx: discord.ApplicationContext):
        latency_ms = get_latency_ms(ctx.bot)
        embed = discord.Embed(
            title="Pong!",
            description=f"Latency: {latency_ms} ms"
        )
        logging.info(f"/ping: latency is {latency_ms} ms")

        await ctx.respond(embed=embed)

    @commands.slash_command(name="oss", description="Open-Source software and licenses")
    async def oss(self, ctx: discord.ApplicationContext):
        embed = SafeEmbed(
            title="Open-Source software and licenses",
            description="Information on open-source software used, and source for Ampere",
            color=discord.Colour.orange()
        )

        with json_open("oss_libs.json", "r") as info:
            for lib in info:
                lib_name = lib["name"]
                lib_info = f"""{lib["description"]}
**Copyright notice**: 
{lib["copyright-notice"]}
Licensed under {lib['license']}
**License URL**: {lib["license-url"]}
**Source**: {lib["source"]}  
"""
                embed.safe_add_field(
                    lib_name,
                    lib_info
                )

        with json_open("bot_oss.json", "r") as oss_json:
            license = oss_json["license"]
            source = oss_json["source"]
            license_url = oss_json["license_url"]
            copyright_notice = oss_json["copyright_notice"]
            embed.safe_add_field(
                "Ampere source and license",
                f"Licensed under {license} - {license_url}\n{copyright_notice}\n{source}"
            )
        await ctx.respond(embed=embed)

    @commands.slash_command(name="help", description="Displays a list of commands for Ampere")
    async def help(self, ctx: discord.ApplicationContext):

        with json_open("bot_help.json", "r") as help_data:
            about = help_data["about"]
            embed = SafeEmbed(
                title=about["name"],
                description=about["description"]
            )
            command_categories = help_data["command_categories"]
            for item in command_categories.items():
                category = item[0]
                cat_commands = item[1]
                desc = ""
                for item2 in cat_commands.items():
                    desc += f"{item2[0]}: {item2[1]}\n"

                embed.safe_add_field(
                    category,
                    desc
                )

            embed.safe_add_field(
                "Invite link",
                "https://dsc.gg/ampere"
            )

            embed.safe_add_field("Source", "https://github.com/czlucius/ampere")
            embed.safe_add_field("Created by", "lcz5#3392")

        await ctx.respond(embed=embed)