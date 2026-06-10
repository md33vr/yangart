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
    BASE_URL = "https://danbooru.donmai.us/posts.json"
    def __init__(self, bot) -> None:
        self.bot = bot
    

    @app_commands.command(
        name = "random_art",
        description= "Give a random art, from all resourses"
    )
    @app_commands.guilds(GUILD)
    async def random_art(self, interaction: discord.Interaction,tags: str) -> None:
        DEFAULT_LIMIT = 1
        fx_tags = re.sub(r' ', '_', tags).replace(":", " ")
        await interaction.response.defer()
        print(fx_tags)
        params = {
            "tags": fx_tags,
            "limit": DEFAULT_LIMIT,
            "random": True,
            "rating": "g"
            
            }
        headers = {
        "user-agent": "prop.spell"
    }
        with requests.Session() as r:
            r.headers.update(headers)
 
            try:
                response = r.get(self.BASE_URL, params= params)
                response.raise_for_status()
                data = response.json()
            
                if not data:
                    await interaction.followup.send("Empty page")
                    return None
                
                post = data[0] 
                 
                RATING = post["rating"]               
                print(RATING) 
                image_url = post["file_url"]
                print(image_url)
            
                await interaction.followup.send(image_url)   
                    
                    
                    
            except requests.RequestException as e:
                print(f"request error: {e}")
                

async def setup(bot) -> None:
    await bot.add_cog(Artgrabber(bot))


