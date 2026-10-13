import psycopg
from psycopg.rows import dict_row
import config

async def get_connection():
    return await psycopg.AsyncConnection.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        row_factory=dict_row
    )
