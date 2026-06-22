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
            guild = insert(GuildsOrm).values(guild_id = guild_id, guild_name = guild_name,bot_instance_id = bot_instance_id)
            session.add(guild)
            await session.flush()
            await session.commit()

    @staticmethod
    async def update_chanell(guild_id: int,channel: ChannelType, chanell_id: int):
        async with session_factory() as session:
            if channel is ChannelType.nsfw:
                stmt = insert(GuildSettingsOrm).values(guild_id = guild_id, nsfw_channel_id=chanell_id)
                stmt = stmt.on_duplicate_key_update(nsfw_channel_id = stmt.inserted.nsfw_channel_id)
                session.add(stmt)
                await session.flush()
                await session.commit()


    @staticmethod
    async def select_channel(guild_id: int, channel: ChannelType):
        async with session_factory() as session:
            if channel is ChannelType.nsfw:
                query= (select(GuildSettingsOrm.nsfw_channel_id).where(GuildSettingsOrm.guild_id == guild_id))
                res = await session.execute(query)
                return res.scalar_one_or_none()