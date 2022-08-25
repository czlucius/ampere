import logging
import discord
import json

from commands.basecog import BaseCog
from discord.ext import commands

from functions.io import json_open
from ui.safeembed import SafeEmbed
from functions.general import get_latency_ms

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

        with json_open("oss_libs.json", "r") as info:
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
