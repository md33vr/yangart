import logging

import discord
import requests
from discord import app_commands
from discord.ext import commands

from config import GUILD

log = logging.getLogger(__name__)


class Artgrabber(commands.Cog, name="art_grabber"):
    BASE_URL = "https://danbooru.donmai.us"
    HEADERS = {"user-agent": "prop.spell"}

    def __init__(self, bot) -> None:
        self.bot = bot
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    @app_commands.command(
        name="random_art",
        description="Give a random art, from all resources",
    )
    @app_commands.guilds(GUILD)
    async def random_art(self, interaction: discord.Interaction, tags: str) -> None:
        await interaction.response.defer()

        query = tags.replace(" ", "_").replace(":", " ")
        params = {"tags": query, "limit": 1, "random": True, "rating": "g"}

        posts = self.get_data("/posts.json", params)
        if not posts:
            await interaction.followup.send("Empty page")
            return

        await interaction.followup.send(posts[0]["file_url"])

    def get_data(self, ex_url: str, params: dict):
        try:
            response = self.session.get(self.BASE_URL + ex_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            log.error("request error: %s", e)
            return None


async def setup(bot) -> None:
    await bot.add_cog(Artgrabber(bot))
