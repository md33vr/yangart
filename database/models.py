import datetime
import enum
from typing import Annotated, Optional

from sqlalchemy import (
    BigInteger,
    ForeignKey,
    String,
    UniqueConstraint,   
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db import Base


intpk = Annotated[int, mapped_column(primary_key=True)]
snowflake = Annotated[int, mapped_column(BigInteger)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("UTC_TIMESTAMP()"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("UTC_TIMESTAMP()"),
    onupdate=datetime.datetime.utcnow,
)]


class GuildsOrm(Base):
    __tablename__ = "guilds"

    guild_id: Mapped[snowflake] = mapped_column(primary_key=True)
    guild_name: Mapped[str] = mapped_column(String(116))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    bot_instance_id: Mapped[snowflake]

class Locate(enum.Enum):
    en = "english"
    ru = "russian" 

class ChannelType(enum.Enum):
    nsfw = "nsfw_channel"
    welcome = "welcome_channel"
    logs = "log_channel"

class AccessLvl(enum.Enum):
    lvl_1, lvl_2, lvl_3, lvl_4, lvl_5, lvl_6, mod, admin = 1, 2, 3, 4, 5, 6, 7, 8

class GuildSettingsOrm(Base):
    __tablename__ = "guild_settings"
    
    guild_id: Mapped[int] = mapped_column(ForeignKey("guilds.guild_id", ondelete="CASCADE"), primary_key=True)
    
    
    locate: Mapped[Locate] = mapped_column(default= Locate.ru)
    log_channel_id: Mapped[Optional[snowflake]]
    welcome_channel_id: Mapped[Optional[snowflake]]
    nsfw_channel_id: Mapped[Optional[snowflake]]
    is_welcome_enb: Mapped[bool] = mapped_column(default= False)
    is_logging_enb: Mapped[bool] = mapped_column(default= False)
    owner_id: Mapped[snowflake]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class AccessPullOrm(Base):
    __tablename__ = "access_pull"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[snowflake]= mapped_column(ForeignKey("guilds.guild_id", ondelete="CASCADE"))
    assigned_by: Mapped[snowflake]
    user_id: Mapped[snowflake]
    access_lvl: Mapped[AccessLvl]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    __table_args__ = UniqueConstraint("guild_id", "user_id")
    
