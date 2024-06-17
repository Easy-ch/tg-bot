import asyncpg
from config import DATABASE_URL
import asyncio
async def create_table():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS course (
            id SERIAL PRIMARY KEY,
            value REAL NOT NULL
        )
    ''')
    await conn.close()

async def set_course(value):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('INSERT INTO course (value) VALUES ($1)', value)
    await conn.close()

async def get_course():
    conn = await asyncpg.connect(DATABASE_URL)
    row = await conn.fetchrow('SELECT value FROM course ORDER BY id DESC LIMIT 1')
    await conn.close()
    return row['value'] if row else None
asyncio.get_event_loop().run_until_complete(create_table())
