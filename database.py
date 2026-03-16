import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "applications.db")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                full_name TEXT,
                phone TEXT,
                direction TEXT,
                technologies TEXT,
                portfolio TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def save_application(user_id: int, username: str, data: dict) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO applications (user_id, username, full_name, phone, direction, technologies, portfolio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            username or "",
            data.get("full_name", ""),
            data.get("phone", ""),
            data.get("direction", ""),
            data.get("technologies", ""),
            data.get("portfolio", ""),
        ))
        await db.commit()
        return cursor.lastrowid


async def get_all_applications() -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT * FROM applications ORDER BY created_at DESC
        """) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def get_application_count() -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM applications") as cursor:
            row = await cursor.fetchone()
            return row[0]
