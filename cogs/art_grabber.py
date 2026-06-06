import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from config import GUILD

import requests


class Artgrabber(commands.Cog, name = "art_grabber"):

    BASE_URL = "https://danbooru.donmai.us/posts.json"
    def __init__(self, bot) -> None:
        self.bot = bot
    

    @app_commands.command(
        name = "random_art",
        description= "Give a random art, from all resourses"
    )
    @app_commands.guilds(GUILD)
    async def random_art(self, intraction: discord.Interaction,tag: str) -> None:
        BAN_TAGS = ["guro", "explict", "sex"]
        DEFAULT_LIMIT = 1
        params = {
            "tags": tag,
            "limit": DEFAULT_LIMIT,
            "random": True
            }
        headers = {
        "user-agent": "prop.spell"
    }
        with requests.Session() as r:
            # добавляем имя для запроса
            r.headers.update(headers)
 
            try:
                response = r.get(self.BASE_URL, params= params)
                response.raise_for_status()
                data = response.json()
                # Проверка на пустую страницу
                if not data:
                    await intraction.message.fetch("Empty page")
                # записываем 1й пост,теги и сравниваем их с бан листом      
                post = data[0]   
                RATING = post["information"]["rating"]
                if RATING == "Explict" or RATING == "Questionable" :
                    print(RATING)
                    await intraction.message.fetch("18+")
                image_url = post["file_url"]
                await intraction.response.send_message(image_url)
            except requests.RequestException as e:
                print(f"request error: {e}")
                

async def setup(bot) -> None:
    await bot.add_cog(Artgrabber(bot))


