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
        fx_tags = re.sub(r' ', '_', tags).split(":")
        print(fx_tags)
        params = {
            "tags": fx_tags,
            "limit": DEFAULT_LIMIT,
            "random": True,
            
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
                print(str(data))
                if not data:
                    await interaction.response.send_message("Empty page")
                    
                post = data[0] 
                print(str(post))  
                RATING = post["rating"]
                
                print(RATING)
                print(post["file_url"])
                # while RATING in ("e", "q"):
                #     n = 1
                #     post = data[1]
                #     n +=1

                image_url = post["file_url"]
                await interaction.response.send_message(image_url)   
                    
                    
                    
            except requests.RequestException as e:
                print(f"request error: {e}")
                

async def setup(bot) -> None:
    await bot.add_cog(Artgrabber(bot))


