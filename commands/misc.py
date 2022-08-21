import logging
import discord
import json

from commands.basecog import BaseCog
from discord.ext import commands

from ui.safeembed import SafeEmbed
from functions.general import get_latency_ms

SOURCE_URL = "https://github.com/czlucius/ampere"
LICENSE = "GNU AGPL v3.0 License"
LICENSE_URL = "https://www.gnu.org/licenses/agpl-3.0-standalone.html"  # TODO please change this
COPYRIGHT_NOTICE = "Copyright (c) 2022 Lucius (lcz5#3392)"


class Misc(BaseCog):

    def __init__(self, bot):
        self.bot = bot

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

        with open("bot_oss.json", "r") as raw:
            raw_text = raw.read()
            info = json.loads(raw_text)
            for lib in info:
                embed.safe_add_field(
                    lib["name"],
                    lib["description"]
                )
                embed.safe_add_field(
                    f"Licensed under {lib['license']}",
                    lib["license-url"],
                    True
                )
                embed.safe_add_field(
                    "Source",
                    lib["source"],
                    True
                )
                embed.safe_add_field(
                    "Copyright Notice",
                    lib["copyright-notice"],
                    True
                )
        embed.safe_add_field(
            "Ampere source and license",
            f"Licensed under {LICENSE} - {LICENSE_URL}\n{COPYRIGHT_NOTICE}\n{SOURCE_URL}"
        )
        await ctx.respond(embed=embed)
