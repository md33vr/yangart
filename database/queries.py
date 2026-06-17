from database.db import engine,session_factory, Base
import database.models
from database.models import ChannelType, GuildSettingsOrm


class AsyncOrm:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    

    @staticmethod
    async def update_chanell(guild_id: int,channel: ChannelType, chanell_id: int):
        async with session_factory() as session:
            if channel is ChannelType.nsfw:
                nsfw_channel = GuildSettingsOrm(guild_id = guild_id, nsfw_channel_id=chanell_id)
                session.add(nsfw_channel)
                await session.flush()
                await session.commit()