import aiomysql
from loader import loop



async def connect():
    return await aiomysql.create_pool(
        host=,
        port=,
        username=,
        password=,
        autocommit = True,
        pool_recycle=100
    )
db_connect = loop.run_until_complete(connect())