import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from config import GUILD

import logging
import re 

import requests


class Artgrabber(commands.Cog, name = "art_grabber"):
    log = logging.getLogger(__name__)
    headers = {
        "user-agent": "prop.spell"
    }
    BASE_URL = "https://danbooru.donmai.us"
    def __init__(self, bot) -> None:
        self.bot = bot
        self.r = requests.Session()
        self.r.headers.update(self.headers)
    @app_commands.command(
        name = "random_art",
        description= "Give a random art, from all resourses"
    )
    @app_commands.guilds(GUILD)
    async def random_art(self, interaction: discord.Interaction,tags: str) -> None:
        DEFAULT_LIMIT = 1
        ex_url = "/posts.json"
        fx_tags = re.sub(r' ', '_', tags).replace(":", " ")
        await interaction.response.defer()
        print(fx_tags)
        params = {
            "tags": fx_tags,
            "limit": DEFAULT_LIMIT,
            "random": True,
            "rating": "g"
            
            }
        data = self.get_data(ex_url, params = params)
               
        if not data:
            await interaction.followup.send("Empty page")
            return None
                
        post = data[0] 
        image_url = post["file_url"]
        print(image_url)
            
        await interaction.followup.send(image_url)   
    

    def get_data(self,ex_url: str, params: dict):
        url = self.BASE_URL + ex_url
        try:
            response = self.r.get(url, params = params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"request error: {e}")
        

async def setup(bot) -> None:
    await bot.add_cog(Artgrabber(bot))

# Нужна команда на реально рандомный арт
# Команда с рандомным автором + о нем
