import discord
from config import TOKEN, GUILD
from discord.ext import commands
from discord import app_commands
from database.queries import AsyncOrm



intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

COG = "art_grabber"

@bot.event
async def on_ready():
    
    await AsyncOrm.create_tables()

    try:
        await bot.load_extension(f"cogs.{COG}")
        
        print(f"Загружен ког: {COG}")
    except Exception as e:
        print(f"Ошибка загрузки {COG}: {e}")
    await bot.tree.sync(guild=GUILD)
    print(f"Logged in as {bot.user}")


bot.run(TOKEN)
