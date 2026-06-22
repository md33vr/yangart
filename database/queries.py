from sqlalchemy import select

from database.db import engine,session_factory, Base
import database.models
from sqlalchemy.dialects.mysql import insert
from database.models import ChannelType, GuildSettingsOrm, GuildsOrm


class AsyncOrm:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    

    @staticmethod
    async def add_guild(guild_id: int, guild_name: str, bot_instance_id: int):
        async with session_factory() as session:
            stmt=(GuildsOrm(guild_id = guild_id, guild_name = guild_name,bot_instance_id = bot_instance_id))
            session.add(stmt)
            await session.flush()
            await session.commit()

    @staticmethod
    async def update_chanell(guild_id: int,channel: ChannelType, chanell_id: int):
        async with session_factory() as session:
                settings = await session.get(GuildSettingsOrm, guild_id)
                if settings:
                    setattr(settings, f"{channel.value}_id", chanell_id)
                else:
                    new = GuildSettingsOrm(guild_id=guild_id)
                    setattr(new, f"{channel.value}_id", chanell_id)
                    session.add(new)
                await session.commit()



    @staticmethod
    async def select_channel(guild_id: int, channel: ChannelType):
        async with session_factory() as session:
            if channel is ChannelType.nsfw:
                query= (select(GuildSettingsOrm.nsfw_channel_id).where(GuildSettingsOrm.guild_id == guild_id))
                res = await session.execute(query)
                return res.scalar_one_or_none()