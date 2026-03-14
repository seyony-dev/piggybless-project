import aiosqlite
from typing import List

DB_PATH = "users.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL
            )
            '''
        )
        await db.commit()


async def add_user(user_id: int, chat_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            '''
            INSERT OR IGNORE INTO users (user_id, chat_id)
            VALUES (?, ?)
            ''',
            (user_id, chat_id)
        )
        await db.commit()


async def get_all_users() -> List[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT user_id, chat_id FROM users') as cursor:
            rows = await cursor.fetchall()
            return [{"user_id": row[0], "chat_id": row[1]} for row in rows]
