import discord
from config import TOKEN, GUILD
from discord.ext import commands
from discord import app_commands



intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

COGS = ["art_grabber"]

@bot.event
async def on_ready():
    for cog in COGS:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"Загружен ког: {cog}")
        except Exception as e:
            print(f"Ошибка загрузки {cog}: {e}")
    await bot.tree.sync(guild=GUILD)
    print(f"Logged in as {bot.user}")


bot.run(TOKEN)
