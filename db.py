import asyncpg
import logging

logger = logging.getLogger(__name__)

class Database:
    _pool = None
    def init(self,host,user,password,database) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database

            

    @classmethod
    async def connect(cls, **kwargs):
        if cls._pool is None:
            try:
                cls._pool = await asyncpg.create_pool(**kwargs)
                logger.info("Database connection pool created successfully")

            except Exception as e:
                logger.error(f"Failed to create database connection pool: {e}")
                logger.info(cls._pool)
                cls._pool = None
        return cls._pool
    @classmethod
    async def close(cls):
        if cls._pool is not None:
            await cls._pool.close()
            cls._pool = None
    
    @classmethod
    async def fetchrow(cls, query, *args):
        if cls._pool is None:
            raise RuntimeError("Connection pool is not initialized")
        async with cls._pool.acquire() as connection:
            return await connection.fetchrow(query, *args)
    
    @classmethod
    async def execute(cls, query, *args):
        if cls._pool is None:
            raise RuntimeError("Connection pool is not initialized")
        async with cls._pool.acquire() as connection:
            return await connection.execute(query, *args)
    
    @classmethod
    async def fetch(cls, query, *args):
        if cls._pool is None:
            raise RuntimeError("Connection pool is not initialized")
        async with cls._pool.acquire() as connection:
            return await connection.fetch(query, *args)

class Course:
    @classmethod
    async def create_table(cls):
        query = """
            CREATE TABLE IF NOT EXISTS course (
            id INT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
            value REAL NOT NULL );
            """
        return await Database.execute(query)
    
    @classmethod
    async def set_course(cls, value):
        query = """ 
            INSERT INTO course (id, value) VALUES (1, $1)
            ON CONFLICT (id) DO UPDATE SET value = EXCLUDED.value;
        """  
        return await Database.execute(query, value)
    
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
                order_id VARCHAR(50) NOT NULL,
                description TEXT,
                status VARCHAR(50) NOT NULL,  
                access_password VARCHAR(255) NOT NULL, 
                image TEXT 
            );
        """
        return await Database.execute(query)
    
    @classmethod
    async def add_order(cls, order_id, description, status, access_password,image_path):
        query = 'INSERT INTO orders (order_id, description, status, access_password,image) VALUES ($1, $2, $3, $4,$5)'
        return await Database.execute(query, order_id, description, status, access_password,image_path)

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
    async def get_order(cls, order_id):
        query = 'SELECT * FROM orders WHERE order_id = $1'
        row = await Database.fetchrow(query, order_id)
        return row
    
    @classmethod
    async def remove_order(cls, order_id):
        query = 'DELETE FROM orders WHERE order_id = $1'
        return await Database.execute(query, order_id)
    
    @classmethod
    async def change_status_order(cls, order_id, status):
        query = 'UPDATE orders SET status = $2 WHERE order_id = $1'
        return await Database.execute(query, order_id, status)