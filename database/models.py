import datetime
import enum
from typing import Annotated, Optional

from sqlalchemy import (
    BigInteger,
    ForeignKey,   
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base


intpk = Annotated[int, mapped_column(primary_key=True)]
snowflake = Annotated[int, mapped_column(BigInteger)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )]

class GuildsOrm(Base):
    __tablename__ = "guilds"

    guild_id: Mapped[snowflake] = mapped_column(primary_key=True)
    guild_name: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    bot_instance_id: Mapped[snowflake]

class Locate(enum.Enum):
    en = "english"
    ru = "russian" 

class GuildSettings(Base):
    __tablename__ = "guild_settings"
    
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.guild_id", 
                                                     ondelete="CASCADE"),
                                                     primary_key=True)

    locate: Mapped[Locate]
    log_channel_id: Mapped[snowflake]
    welcome_channel_id: Mapped[snowflake]
    nsfw_channel_id: Mapped[snowflake]
    is_welcome_enb: Mapped[bool]
    is_logging_enb: Mapped[bool]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
