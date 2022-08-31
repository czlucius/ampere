import logging
import discord

from urllib.error import HTTPError
from libretranslatepy import LibreTranslateAPI
from commands.basecog import BaseCog
from discord.ext import commands

from exceptions import InvalidOptionException
from functions.io import json_open
from ui.safeembed import SafeEmbed
from functions.general import get_latency_ms


lt_client = LibreTranslateAPI("http://localhost:5001")
# Example: [{'code': 'en', 'name': 'English'}, {'code': 'ar', 'name': 'Arabic'}, {'code': 'zh', 'name': 'Chinese'}, {'code': 'fr', 'name': 'French'}, {'code': 'de', 'name': 'German'}, {'code': 'hi', 'name': 'Hindi'}, {'code': 'id', 'name': 'Indonesian'}, {'code': 'ga', 'name': 'Irish'}, {'code': 'it', 'name': 'Italian'}, {'code': 'ja', 'name': 'Japanese'}, {'code': 'ko', 'name': 'Korean'}, {'code': 'pl', 'name': 'Polish'}, {'code': 'pt', 'name': 'Portuguese'}, {'code': 'ru', 'name': 'Russian'}, {'code': 'es', 'name': 'Spanish'}, {'code': 'tr', 'name': 'Turkish'}, {'code': 'vi', 'name': 'Vietnamese'}]
lt_raw_langs = lt_client.languages()
lt_langs = {}
for i in lt_raw_langs:
    lt_langs[i["name"]] = i["code"]
lt_source_langs = lt_langs.copy()
lt_source_langs["Auto Detect"] = "auto"

class Misc(BaseCog):

    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name="translate", description="Translate between languages")
    @discord.option("text", description="Text to translate")
    @discord.option("from", description="Language you're translating from", choices = lt_source_langs.keys())
    @discord.option("to", description="Language you're translating to", choices = lt_langs.keys())
    async def translate(self, ctx: discord.ApplicationContext, text: str, from_lang: str, to_lang: str):
        try:
            if from_lang not in lt_source_langs:
                raise InvalidOptionException("Invalid source language!")
            if to_lang not in lt_langs:
                raise InvalidOptionException("Invalid target language!")
            translated = lt_client.translate(text, from_lang, to_lang)
            embed = SafeEmbed(
                title="Translated text",
                description=translated
            )
            embed.safe_add_field("Original text", text)
            embed.safe_add_field("From", from_lang)
            embed.safe_add_field("To", to_lang)
        except InvalidOptionException as err:
            embed = SafeEmbed(
                title="Error!",
                description=str(err),
                colour=discord.Colour.red()
            )
            logging.error(f"/translate: error occurred - {err} - {type(err)} - {err.with_traceback()}")
        except HTTPError:
            embed = SafeEmbed(
                title="Error!",
                description="API endpoint error",
                colour=discord.Colour.red()
            )

        await ctx.respond(embed=embed)



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
