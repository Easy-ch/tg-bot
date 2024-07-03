import asyncpg
import asyncio
from config import POSTGRES_HOST,POSTGRES_PASSWORD,POSTGRES_USER,POSTGRES_DATABASE



# import asyncio
class Database:
    _pool = None
    @classmethod
    async def connect(cls,**kwargs):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(           
                host=POSTGRES_HOST,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                database=POSTGRES_DATABASE)
        return cls._pool
    @classmethod
    async def close(cls):
        if cls._pool is not None:
            await asyncpg.close()
            cls._pool = None
    @classmethod
    async def fetchrow(cls,query,*args):
        async with cls._pool.acquire() as connection:
            return await connection.fetchrow(query,*args)
    @classmethod
    async def execute(cls,query,*args):
        async with cls._pool.acquire() as connection:
            return await connection.execute(query,*args)
    @classmethod
    async def fetch(cls,query,*args):
        async with cls._pool.acquire() as connection:
            return await connection.fetch(query,*args)

class Course:
    @classmethod 
    async def create_table(cls):
        query = """
    CREATE TABLE IF NOT EXISTS course (
            id SERIAL PRIMARY KEY,
            value REAL NOT NULL)
    """
        return await Database.execute(query)
    @classmethod
    async def set_course(cls,value):
        query = 'INSERT INTO course (value) VALUES ($1)'
        return  await Database.execute(query,value)
    @classmethod
    async def get_course(cls):
        query = 'SELECT value FROM course ORDER BY id DESC LIMIT 1'
        row = await Database.fetchrow(query)
        return row['value'] if row else None
    
class Order:
    @classmethod
    async def create_table(cls):
        query = """
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY, 
        order_id  VARCHAR(50) NOT NULL,
        description TEXT,
        status VARCHAR(50) NOT NULL,  
        access_password VARCHAR(255) NOT NULL  
    );
    """
        return await Database.execute(query)
    @classmethod
    async def add_order(cls,order_id,description,status,access_password):
        query ='INSERT INTO orders (order_id,description,status,access_password) VALUES ($1,$2,$3,$4)'
        return await Database.execute(query,order_id,description,status,access_password)

    @classmethod
    async def password_valid(cls, order_id, access_password):
        query = 'SELECT 1 FROM orders WHERE order_id = $1 AND access_password = $2'
        row = await Database.fetchrow(query, order_id, access_password)
        return row is not None
    
    @classmethod
    async def order_exists(cls, order_id):
        query = 'SELECT 1 FROM orders WHERE order_id = $1'
        row = await Database.fetchrow(query, order_id)
        return row is not None


    @classmethod
    async def get_order(cls,order_id):
        query = 'SELECT * FROM orders WHERE order_id = $1'
        row = await Database.fetchrow(query,order_id)
        return row
    
    @classmethod 
    async def remove_order(cls,order_id):
        query = """
        DELETE FROM orders
        WHERE order_id = $1;
        """
        return await Database.execute(query,order_id)
    
    @classmethod
    async def change_status_order(cls,order_id,status):
        query = """
        UPDATE orders
        SET status = $2
        WHERE order_id = $1
        """
        return await Database.execute(query,order_id,status)
    
