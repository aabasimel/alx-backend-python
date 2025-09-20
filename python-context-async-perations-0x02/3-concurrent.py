##!/usr/bin/env python3
"""
3-concurrent.py
Run multiple database queries concurrently using asyncio and aiosqlite
"""

import asyncio
import aiosqlite

DB_PATH = "users.db"  
async def async_fetch_users():
    """Fetch all users from the users table."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            return [dict(row) for row in results]

async def async_fetch_older_users():
    """Fetch users older than 40 from the users table."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            return [dict(row) for row in results]

async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather."""
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All Users:")
    for user in all_users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
