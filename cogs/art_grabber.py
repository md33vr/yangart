import logging

import discord
import requests
from discord import app_commands
from discord.ext import commands

from config import GUILD
from database.queries import AsyncOrm
from database.models import ChannelType

log = logging.getLogger(__name__)


class Artgrabber(commands.Cog, name="art_grabber"):

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await AsyncOrm.add_guild(guild.id, guild.name, self.bot.user.id)

    NSFW_URL = "https://danbooru.donmai.us"
    SAFE_URL = "https://safebooru.donmai.us/"
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
        base_url
        params = {"tags": query, "limit": 1, "random": True}
        r_channel_id= await AsyncOrm.select_channel(interaction.guild_id, ChannelType.nsfw)
        print(r_channel_id)
        print(interaction.channel_id)
        if interaction.channel_id == r_channel_id:
            base_url =  self.NSFW_URL
        else:
            base_url = self.SAFE_URL

        print(str(params))
        
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
    @app_commands.command(
        name="setnsfw",
        description="test",
    )
    @app_commands.guilds(GUILD)
    async def set_nsfw(self, interaction: discord.Interaction, channel_type: ChannelType ):
        await interaction.response.defer()
        print(interaction.channel_id)
        try:
            await interaction.channel.edit(nsfw= True)
            await AsyncOrm.update_chanell(interaction.guild_id,channel_type, interaction.channel_id)
            await interaction.followup.send("канал: " + str(interaction.channel_id) + " установлен как nsfw")
        except:
            await interaction.followup.send("не удалось установить nsfw канал")
    
    # async def set_general(self, interaction: discord.Interaction, channel_type: ChannelType ):
    #     await interaction.response.defer()
    #     print(interaction.channel_id)
    #     await AsyncOrm.update_chanell(interaction.guild_id,channel_type, interaction.channel_id)
    #     await interaction.followup.send("канал: " + str(interaction.channel_id) + "установлен как nsfw")   






async def setup(bot) -> None:
    await bot.add_cog(Artgrabber(bot))
