from dotenv import load_dotenv
import discord
import os
load_dotenv()
from pydantic_settings import BaseSettings, SettingsConfigDict
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
GUILD = discord.Object(id=GUILD_ID)
API_KEY = os.getenv("API_KEY")
USER_ID = int(os.getenv("USER_ID"))
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str



    @property
    def DATABASE_URL(self):
        return f"mariadb+aiomysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}" 
    

settings = Settings()